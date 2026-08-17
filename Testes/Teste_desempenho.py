import sys
import pandas as pd
import numpy as np

# =====================================================
# ADICIONA O CAMINHO DA BIBLIOTECA STM AI RUNNER
# =====================================================
caminho_da_biblioteca = r"C:\ST\STEdgeAI\4.0\scripts\ai_runner"
sys.path.append(caminho_da_biblioteca)

from stm_ai_runner import AiRunner

# =====================================================
# CONFIGURAÇÕES
# =====================================================
CSV_PATH = r"C:\Users\Usuário\Documents\test_vectors_int8.csv"
WINDOW_SIZE = 306
SERIAL_PORT = "serial:COM3:115200"

# =====================================================
# LER CSV
# =====================================================
print("Lendo CSV...")

df = pd.read_csv(CSV_PATH)

# Converte para numpy
data = df.values.astype(np.int16)

# Entradas
X = data[:, :WINDOW_SIZE].astype(np.int8)

# Apenas a primeira amostra
ecg = X[0].reshape(1, WINDOW_SIZE, 1)

print("Primeira amostra carregada.")
print("Shape da entrada:", ecg.shape)

# =====================================================
# CONECTAR AO STM32
# =====================================================
print("\nConectando ao STM32...")

runner = AiRunner()
runner.connect(SERIAL_PORT)

print("Conectado com sucesso!")

# =====================================================
# RESUMO DO MODELO
# =====================================================
print("\n================ MODEL SUMMARY ================\n")
runner.summary()

# =====================================================
# INFERÊNCIA COM PROFILING POR CAMADA
# =====================================================
print("\n================ INFERÊNCIA ================\n")

inputs = [ecg]

outputs, profiler = runner.invoke(
    inputs,
    mode=AiRunner.Mode.PER_LAYER
)

# =====================================================
# PROFILING
# =====================================================
print("\n================ PROFILING ================\n")

runner.print_profiling(
    inputs,
    profiler,
    outputs
)

# =====================================================
# SAÍDA DA REDE
# =====================================================
print("\n================ OUTPUT ================\n")

output_vec = outputs[0].reshape(-1)

print("Saída bruta:")
print(output_vec)

pred = np.argmax(output_vec)

print("\nClasse prevista:", pred)