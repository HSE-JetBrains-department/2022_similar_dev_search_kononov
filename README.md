# 2022_similar_dev_search_kononov

### Описание проекта

Этот проект нужен, чтобы искать похожих разработчиков. **Схожесть** — это метрика, которая может
вычисляться на основе разных данных, например:

* Языки программирования.
* Пересечение по импортам, именам переменных (которые можно распарсить в несколько слов).
* Использование одинаковых библиотек.

### Этапы проекта

Ориентировочно проект будет состоять из 7 этапов

1) **Discover**: Найти репозитории на гитхабе.
2) **Clone**: Скопировать репозитории к себе.
3) **Handle VCS**: Нужно будет извлечь коммиты в формате JSON'а, содержащие:
    * blob_id,
    * путь коммита,
    * хэш коммита,
    * кол-во удалённых, изменённых и добавленных строк кода,
    * почта и имя автора,
    * ссылку на репозиторий.
4) **Classify**: Распознать язык програмирования. Использовать enry[^1].
5) **Filter**: Оставить только нужные файлы (файлы языков программирования).
6) **Parse**: Представить код в виде AST-дерева, используя tree-sitter[^2].
7) **Similar dev search**: Имплементиовать поиск по полученным данным.

#### Сравнение разработчиков

Для каждого разработчиков будет два вектора:

1) вектор языков программирования - сколько строк, байтов было написано разработчиком на конкретном
   языке.
2) векторы имен переменных и импортов.

### Оценивание проекта

Оценка за проект складывается из выполненных этапов: Grade = github_api * **0.15** + git * **0.25**

+ enry[^1] * **0.2** + tree_sitter[^2] * **0.25** + similar_dev_search * **0.15**

[^1]: классификатор языков программирования https://github.com/go-enry/go-enry
[^2]: библиотека для извлечения AST из кода https://github.com/tree-sitter/tree-sitter

### Результаты

Топ 100 репозиториев при вызове `extract_stargazers` с аргументами:

```python
extract_stargazers(repo_name="scikit-learn/scikit-learn",
                   key=...,
                   repos_per_user=100,
                   stargazers_number=1000,
                   top_repos_number=100,
                   requests_per_page=100)
```

```json
{
  "pandas-dev/pandas": 77,
  "tensorflow/tensorflow": 65,
  "CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers": 63,
  "ipython/ipython": 62,
  "scipy/scipy": 59,
  "d3/d3": 57,
  "numpy/numpy": 57,
  "VowpalWabbit/vowpal_wabbit": 51,
  "twbs/bootstrap": 51,
  "donnemartin/system-design-primer": 47,
  "huggingface/transformers": 45,
  "JuliaLang/julia": 45,
  "pymc-devs/pymc": 41,
  "Textualize/rich": 39,
  "google/jax": 39,
  "keras-team/keras": 39,
  "awesomedata/awesome-public-datasets": 37,
  "josephmisiti/awesome-machine-learning": 37,
  "scikit-image/scikit-image": 37,
  "psf/requests": 35,
  "Theano/Theano": 34,
  "bloomberg/memray": 33,
  "nathanmarz/storm": 33,
  "papers-we-love/papers-we-love": 33,
  "matplotlib/matplotlib": 32,
  "statsmodels/statsmodels": 32,
  "explosion/spaCy": 32,
  "neovim/neovim": 32,
  "dmlc/xgboost": 31,
  "nltk/nltk": 30,
  "pallets/flask": 30,
  "apache/superset": 30,
  "scrapy/scrapy": 29,
  "numba/numba": 29,
  "sindresorhus/awesome": 29,
  "slundberg/shap": 29,
  "django/django": 28,
  "facebookresearch/fastText": 28,
  "impress/impress.js": 28,
  "RaRe-Technologies/gensim": 28,
  "tiangolo/fastapi": 27,
  "norvig/pytudes": 27,
  "3b1b/manim": 27,
  "EbookFoundation/free-programming-books": 27,
  "mwaskom/seaborn": 27,
  "ray-project/ray": 27,
  "pytorch/pytorch": 26,
  "tensorflow/models": 26,
  "spotify/luigi": 26,
  "redis/redis": 24,
  "ant-design/ant-design": 23,
  "python/cpython": 22,
  "fastai/fastbook": 22,
  "pyscript/pyscript": 22,
  "tornadoweb/tornado": 22,
  "HarisIqbal88/PlotNeuralNet": 22,
  "bokeh/bokeh": 22,
  "resume/resume.github.com": 22,
  "networkx/networkx": 22,
  "microsoft/LightGBM": 22,
  "codecrafters-io/build-your-own-x": 22,
  "floodsung/Deep-Learning-Papers-Reading-Roadmap": 22,
  "marcotcr/lime": 22,
  "Homebrew/legacy-homebrew": 22,
  "facebookresearch/faiss": 22,
  "blei-lab/edward": 22,
  "clips/pattern": 22,
  "torvalds/linux": 22,
  "Yelp/mrjob": 21,
  "httpie/httpie": 21,
  "pola-rs/polars": 21,
  "streamlit/streamlit": 21,
  "joblib/joblib": 20,
  "ohmyzsh/ohmyzsh": 20,
  "ibraheemdev/modern-unix": 20,
  "quantopian/zipline": 20,
  "jwasham/coding-interview-university": 20,
  "h5bp/html5-boilerplate": 20,
  "yhat/ggpy": 20,
  "BVLC/caffe": 20,
  "jlevy/the-art-of-command-line": 20,
  "google-research/bert": 20,
  "awesome-selfhosted/awesome-selfhosted": 19,
  "hyperopt/hyperopt": 19,
  "huginn/huginn": 19,
  "sebastianruder/NLP-progress": 19,
  "lisa-lab/pylearn2": 19,
  "isocpp/CppCoreGuidelines": 19,
  "pybrain/pybrain": 19,
  "donnemartin/data-science-ipython-notebooks": 19,
  "klbostee/dumbo": 19,
  "altair-viz/altair": 19,
  "github/gitignore": 19,
  "blaze/blaze": 19,
  "aymericdamien/TensorFlow-Examples": 19,
  "apache/spark": 19,
  "realpython/python-guide": 18,
  "rlabbe/Kalman-and-Bayesian-Filters-in-Python": 18,
  "terryum/awesome-deep-learning-papers": 18
}

```