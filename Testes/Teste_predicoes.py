import sys
import pandas as pd


caminho_da_biblioteca = r"C:\ST\STEdgeAI\4.0\scripts\ai_runner"
sys.path.append(caminho_da_biblioteca)

try:
    from stm_ai_runner import AiRunner
    import time
    import numpy as np
    
    print("FANTÁSTICO! O stm_ai_runner foi importado com sucesso!")
except ModuleNotFoundError as e:
    print(f"Ainda não encontrou. Erro: {e}")

# ==========================
# CONFIGURAÇÕES
# ==========================
CSV_PATH = r"C:\Users\Usuário\Documents\test_vectors_int8.csv"
WINDOW_SIZE = 306

# ==========================
# LER CSV
# ==========================
print("Lendo CSV...")

df = pd.read_csv(CSV_PATH)

# garante numpy int correto
data = df.values.astype(np.int16)

X = data[:, :WINDOW_SIZE].astype(np.int8)
y_real = data[:, WINDOW_SIZE].astype(np.uint8)

print("Total de amostras:", len(X))

# ==========================
# CONECTAR AO STM32
# ==========================
runner = AiRunner()
runner.connect("serial:COM3:115200")

print("Conectado com sucesso!")

# ==========================
# INFERÊNCIA
# ==========================
y_pred = []

print("Iniciando inferência...")

for i in range(len(X)):

    ecg = X[i].reshape(1, 306, 1)

    outputs, profiler = runner.invoke(
        [ecg],
        mode=AiRunner.Mode.IO_ONLY
    )

    output_vec = outputs[0].reshape(-1)  # (5,)
    pred = np.argmax(output_vec)

    y_pred.append(pred)

    print(f"Amostra {i}: Real={y_real[i]} | Pred={pred}")

# ==========================
# RESULTADO FINAL
# ==========================
y_pred = np.array(y_pred)

accuracy = np.mean(y_pred == y_real)

#print("\n===== RESULTADO FINAL =====")
#print("Acurácia:", accuracy)
#print("Total:", len(y_real))

# ==========================
# SALVAR CSV DE RESULTADOS
# ==========================

results_df = pd.DataFrame({
    "real": y_real,
    "pred": y_pred
})

OUTPUT_CSV = r"C:\Users\Usuário\Documents\predicoes_stm32_under_over.csv"

results_df.to_csv(OUTPUT_CSV, index=False)

print(f"\nPrediçoes salvas em: {OUTPUT_CSV}")