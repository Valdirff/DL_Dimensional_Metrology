import cv2
import os

# Pastas
pasta_imagens_ruins = "dataset/ruins/"
pasta_imagens_boas = "dataset/boas/"
pasta_labels = "dataset/labels_ruins/"
pasta_labels_boas = "dataset/labels_boas/"
os.makedirs(pasta_labels, exist_ok=True)
os.makedirs(pasta_labels_boas, exist_ok=True)

# Variáveis globais
drawing = False
ix, iy = -1, -1
boxes = []

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, boxes, img, clone

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img = clone.copy()
            for (xmin, ymin, xmax, ymax) in boxes:
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 0), 2)
            cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 0), 2)
        boxes.append((min(ix, x), min(iy, y), max(ix, x), max(iy, y)))

def salvar_yolo(file_name, boxes, largura, altura):
    txt_path = os.path.join(pasta_labels, file_name.replace(".jpg", ".txt").replace(".png", ".txt"))
    with open(txt_path, "w") as f:
        for (xmin, ymin, xmax, ymax) in boxes:
            x_center = ((xmin + xmax) / 2) / largura
            y_center = ((ymin + ymax) / altura) / altura
            w = (xmax - xmin) / largura
            h = (ymax - ymin) / altura
            f.write(f"0 {x_center} {y_center} {w} {h}\n")


# ====================================================
# 1) ANOTAR IMAGENS RUINS
# ====================================================
arquivos = sorted([f for f in os.listdir(pasta_imagens_ruins) if f.endswith((".jpg", ".png"))])
i = 0

while 0 <= i < len(arquivos):
    file = arquivos[i]
    path = os.path.join(pasta_imagens_ruins, file)
    img = cv2.imread(path)
    clone = img.copy()
    boxes = []

    cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("image", draw_rectangle)

    while True:
        cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):  # salvar e próxima
            salvar_yolo(file, boxes, img.shape[1], img.shape[0])
            print(f"Salvo: {file} -> {len(boxes)} falhas")
            i += 1
            break

        elif key == ord("r"):  # resetar boxes
            img = clone.copy()
            boxes = []
            print("Resetado tudo.")

        elif key == ord("z"):  # desfazer última box
            if boxes:
                boxes.pop()
                img = clone.copy()
                for (xmin, ymin, xmax, ymax) in boxes:
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 0), 2)
                print("Última box removida.")
            else:
                print("Nenhuma box para remover.")

        elif key == ord("b"):  # voltar para anterior
            print("Voltando para imagem anterior...")
            i = max(0, i - 1)
            break

        elif key == ord("q"):  # sair definitivamente
            print("Saindo do programa...")
            cv2.destroyAllWindows()
            exit(0)

    cv2.destroyAllWindows()

# ====================================================
# 2) GERAR TXT VAZIO PARA IMAGENS BOAS
# ====================================================
for file in os.listdir(pasta_imagens_boas):
    if file.endswith((".jpg", ".png")):
        txt_path = os.path.join(pasta_labels_boas, file.replace(".jpg", ".txt").replace(".png", ".txt"))
        if not os.path.exists(txt_path):
            with open(txt_path, "w") as f:
                pass
            print(f"Gerado vazio: {file}")
