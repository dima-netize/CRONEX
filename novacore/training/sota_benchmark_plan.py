from novacore.models.sota_bench import default_external_suites


if __name__ == "__main__":
    print("External benchmark roadmap:")
    for suite in default_external_suites():
        print(f"- {suite.name}: {', '.join(suite.tasks)}")
