# Scalable Data Harvesting for AI
### Presentation: [Scalable Data Harvesting for AI](workshop/presentation_template.pdf)

## Workshop Description
Large scale training sets are the foundation for AI models and their development.
Many AI companies or companies that produce large scale ML/AI models rely at least in part on webscraping frameworks. These frameworks are often required to scrape terabytes worth of data from various sources. In this workshop we will get into one of these, and arguably one of the most popular frameworks: Scrapy.

In the [workshop](./workshop/README.md) folder, you will find a collection of exercises, that will teach you how to create a new scrapy project from scratch and collect documents at high trhoughput rates.

### Setting Up the Environment
Before working on the exercises, we recommend to set up a virtual environment.
PyLadies typically uses `uv` for that.

1. Installing  UV (if not done already)
```bash
pip install uv
```

2. Creating a virtual environment
```bash
uv venv
```

3. Install dependencies
```bash
cd workshop/ # Enter the workspace
uv sync
```

4. Install additional packages as needed
```bash
uv add PACKAGE
```

## Video record
Re-watch [this YouTube stream](https://www.youtube.com/watch?v=0wqXbShaAvU).

## Credits
This workshop was set up by @pyladiesams, @mmbc2008 and @gCaglia.
