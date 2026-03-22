import os, shutil
from sklearn.model_selection import train_test_split

# Pastas atuais
pasta_boas = "dataset/boas"
pasta_ruins = "dataset/ruins"
labels_boas = "dataset/labels_boas"
labels_ruins = "dataset/labels_ruins"

# Pastas destino no formato YOLO
base_out = "dataset_yolo/"
splits = ["train", "val", "test"]

for split in splits:
    os.makedirs(os.path.join(base_out, "images", split), exist_ok=True)
    os.makedirs(os.path.join(base_out, "labels", split), exist_ok=True)

# Lista imagens
boas = [f for f in os.listdir(pasta_boas) if f.endswith((".jpg",".png"))]
ruins = [f for f in os.listdir(pasta_ruins) if f.endswith((".jpg",".png"))]

# Divide cada grupo SEPARADO (70/20/10)
def splitar(lista, test_size=0.1, val_size=0.2):
    train_val, test = train_test_split(lista, test_size=test_size, random_state=42)
    train, val = train_test_split(train_val, test_size=val_size/(1-test_size), random_state=42)
    return train, val, test

boas_train, boas_val, boas_test = splitar(boas)
ruins_train, ruins_val, ruins_test = splitar(ruins)

# Junta resultados
divisoes = {
    "train": [("boas", f) for f in boas_train] + [("ruins", f) for f in ruins_train],
    "val":   [("boas", f) for f in boas_val]   + [("ruins", f) for f in ruins_val],
    "test":  [("boas", f) for f in boas_test]  + [("ruins", f) for f in ruins_test],
}

# Copia arquivos
for split, arquivos in divisoes.items():
    for tipo, img in arquivos:
        if tipo == "boas":
            pasta_img, pasta_lbl = pasta_boas, labels_boas
        else:
            pasta_img, pasta_lbl = pasta_ruins, labels_ruins

        # caminhos origem
        path_img = os.path.join(pasta_img, img)
        nome_txt = img.replace(".jpg",".txt").replace(".png",".txt")
        path_lbl = os.path.join(pasta_lbl, nome_txt)

        # caminhos destino
        out_img = os.path.join(base_out, "images", split, img)
        out_lbl = os.path.join(base_out, "labels", split, nome_txt)

        shutil.copy(path_img, out_img)
        shutil.copy(path_lbl, out_lbl)

print("✅ Dataset balanceado e reorganizado em formato YOLO dentro de 'dataset_yolo/'")
