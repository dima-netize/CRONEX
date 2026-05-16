from novacore.models.novacore import NovaCoreMini


if __name__ == "__main__":
    model = NovaCoreMini()

    programs = [
        "STORE_COLOR C4 | SHIFT N2 | SHIFT N3 | QUERY",
        "PAIR S3 C7 | QUERY S3",
        "PAIR S3 C7 | QUERY C7",
    ]

    for program in programs:
        result = model.run(program)
        print("\nProgram:", program)
        print("Answer:", result.answer)
        print("Verified:", result.verified)
        print("Reason:", result.verifier_reason)
        print("Trace:")
        for step in result.trace:
            print("  -", step)
