## Adding a new sheet

1. To add support for a new sheet you'll need to ensure your data is in a publicly accessible Google sheet. In addition you must have a column called 'SMILES' for the smiles string of the molecule.
2. Edit `sheets.py` to include a new the key of the sheet (you can find this in the url) as well as the sheet_number - that is the position of the sheet you would like to fetch starting from 1 (first sheet)
3. Create a new files in `templates/` to edit the text that is tweeted each time. These templates use [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) so you can include some logic in here - see 'Creating a template' below.
4. Create a workflow in `.github/workflows` (use `malaria.yml` as a template) to set a tweet schedule.


## Creating a template

You can add properties to the tweet either exist as columns in your existing Google Sheet or that have been precomputed.

### Properties from the Google Sheet

To reference properties from the Google sheet simply take the lower case value of the column with any whitespace and symbols removed.

| Column in sheet  | Value in template |
| ------------- | ------------- |
| PubChem CID  | pubchemcid  |
| Pfal IC50 (Ralph)  | pfalic50ralph  |
| LogD 3.0 (Monash) | logd3.0monash |

To reference in a template simply wrap in curly braces

```
PubChem CID: {{ pubchemid }}
```
will render
```
PubChem CID: 123
```

### Precomputed properties

The following properties are precomputed and can be referenced by prefixing with 'properties' e.g., for TPSA you can simply use:

```
TPSA: {{ properties.tpsa }}
```
will render
```
TPSA: 86.22
```

The current list of supported properties are:

| Property | Description |
| ------------- | ------------- |
| molwt | molecular weight |
| hba | hydrogen bond acceptors |
| numrotatablebonds | number of rotatable bonds |
| mollogp | log p |
| hbd | hydrogen bond donors |
| tpsa | topological polar surface area |


