from pathlib import Path

import dev_stats
import enry
import pipeline


# if __name__ == "__main__":
#     fil = {"author": "Ben", "language": "lag", "added": 1, "lines_number": 3,
#            "variables": {"a": 25}, "classes": {"c": 2}, "functions": {"f": 1}}
#     dev_stats.add_file_to_dev_stats(fil)
#     print(dev_stats.stats)


if __name__ == "__main__":
    pipeline.pipeline()


# if __name__ == "__main__":
#     enry.extract_languages(Path("../scikit-learn/sklearn/svm"))
