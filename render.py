from rdkit.Chem import MolFromSmiles
from rdkit.Chem.Descriptors import MolWt, MolLogP, TPSA
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.Lipinski import NumHAcceptors, NumHDonors, NumRotatableBonds

width, height = 500, 500  # width and height of the image


def generate_image(smiles: str):
    """Generates a PNG images from a SMILES string."""
    mol = MolFromSmiles(smiles)  # may raise an exception
    drawing = rdMolDraw2D.MolDraw2DCairo(width, height)
    rdMolDraw2D.PrepareAndDrawMolecule(drawing, mol)
    drawing.WriteDrawingText("molecule.png")


def generate_properties(smiles: str):
    """Generates a set of pre-determined properties for a molecule."""
    mol = MolFromSmiles(smiles)
    return {
        "molwt": MolWt(mol),  # molecular weight
        "hba": NumHAcceptors(mol),  # hydrogen bond acceptors
        "numrotatablebonds": NumRotatableBonds(mol),  # rotatable bonds
        "mollogp": MolLogP(mol),  # log p
        "hbd": NumHDonors(mol),  # hydrogen bond donors
        "tpsa": TPSA(mol),  # polar surface area
    }
