from rdkit.Chem import MolFromSmiles
from rdkit.Chem.Draw import rdMolDraw2D

width, height = 500, 500  # width and height of the image


def generate_image(smiles: str):
    """Generates a PNG images from a SMILES string."""
    mol = MolFromSmiles(smiles)  # may raise an exception
    drawing = rdMolDraw2D.MolDraw2DCairo(width, height)
    rdMolDraw2D.PrepareAndDrawMolecule(drawing, mol)
    drawing.WriteDrawingText("molecule.png")
