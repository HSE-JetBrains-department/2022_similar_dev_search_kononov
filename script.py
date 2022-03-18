import argparse

from extract import repo_to_jsonl

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract repository.")

    parser.add_argument("repo_name", type=str, help="name of extracted repository")
    parser.add_argument("repo_url", type=str, help="url of extracted repository")
    parser.add_argument("json_name", type=str, help="file name where repository data is stored")

    args = parser.parse_args()

    repo_to_jsonl(args.repo_name, args.repo_url, args.json_name)