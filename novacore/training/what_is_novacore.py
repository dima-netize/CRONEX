from novacore.models.capabilities import default_capabilities


if __name__ == "__main__":
    print("NovaCore Mini — що це таке і що вміє:\n")
    for idx, cap in enumerate(default_capabilities(), start=1):
        print(f"{idx}. {cap.name}")
        print(f"   Що вміє: {cap.description}")
        print(f"   Для чого: {cap.use_case}\n")
