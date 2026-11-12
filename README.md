# Playwright Exporter

This tool is used to download data from a few websites: 

### Setup

#### Installing playwright

First, create a new Conda profile for this work. We will call it `playwright_exporter`:

```bash
conda create --name playwright_exporter
```

If needed, update Conda first:

```bash
 conda update -n base -c conda-forge conda
```

To list our environments, do:

```bash
 conda env list
```

Switch to our environment and install the playwright libraries:

```bash
 conda activate playwright_exporter
 conda config --add channels conda-forge
 conda config --add channels microsoft
conda install pytest-playwright
```

Then install the browsers:

```bash
playwright install
```

Happy Hacking!

#### Configuring the environment

##### Installing additional libraries

There are a few other libraries needed before first use

```bash
conda install python-dotenv pandas lxml html5lib beautifulsoup4 numpy pyyaml
```

##### Credentials and settings

Before starting, you would need to supply the following credentials:

- user name (`user`)
- password (`password`)
- Download location (`download_location`): where to store the downloaded files
- Working directory (`working_directory`): where to find the `scraper_functions.py` script

These variables are stored in an `.env` file in the main working directory of the scraper script. The format should look like this:

```.env
user=user@email.com
password=your password
download_location=C:/download/
```
