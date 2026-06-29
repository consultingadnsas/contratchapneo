import docx
import re
import os
import subprocess
import shutil

def extract_tags_grouped_by_paragraph(file_path):
    doc = docx.Document(file_path)
    pattern = re.compile(r'\{\{\s*(.*?)\s*\}\}')
    
    blocks_data = []
    seen_tags = set() # Pour s'assurer qu'on ne demande jamais deux fois la même variable
    
    # Taille maximale pour éviter d'envoyer un paragraphe d'une page entière
    MAX_PARAGRAPH_LENGTH = 400 

    def process_blocks(blocks):
        for block in blocks:
            text = block.text.strip()
            if not text:
                continue
            
            # 1. On cherche toutes les balises dans ce paragraphe
            matches = pattern.findall(text)
            
            if matches:
                tags_in_this_block = []
                
                # 2. On filtre pour ne garder que les NOUVELLES balises
                for match in matches:
                    tag_name = match.strip()
                    if tag_name not in seen_tags:
                        tags_in_this_block.append(tag_name)
                        seen_tags.add(tag_name)
                
                # 3. Si on a trouvé de nouvelles balises, on crée le bloc
                if tags_in_this_block:
                    context_text = text
                    
                    # On tronque si le paragraphe est vraiment trop long
                    if len(context_text) > MAX_PARAGRAPH_LENGTH:
                        # (On pourrait affiner pour ne pas couper au milieu d'une balise, 
                        # mais pour l'instant une simple coupure suffit)
                        context_text = context_text[:MAX_PARAGRAPH_LENGTH] + "..."
                        
                    blocks_data.append({
                        "tags": tags_in_this_block, # Attention, c'est devenu une LISTE !
                        "context": context_text
                    })

    # Parcourir les paragraphes normaux
    process_blocks(doc.paragraphs)

    # Parcourir les tableaux (très fréquents dans les contrats)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                process_blocks(cell.paragraphs)

    return blocks_data


def convert_docx_to_pdf(docx_path, output_dir=None):
    """
    Convertit un fichier .docx en .pdf en utilisant LibreOffice en mode headless.
    Fonctionne sur Linux (Serveur, Docker), macOS et Windows.
    
    :param docx_path: Chemin absolu vers le fichier .docx à convertir
    :param output_dir: Dossier de destination du PDF (par défaut le même dossier que le docx)
    :return: Chemin absolu vers le fichier .pdf généré
    """
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Le fichier source n'existe pas : {docx_path}")
    
    # Par défaut, on enregistre dans le même répertoire que le fichier docx
    if output_dir is None:
        output_dir = os.path.dirname(docx_path) or '.'

    # Détection automatique de l'exécutable LibreOffice (soffice)
    soffice_path = shutil.which('soffice') or shutil.which('libreoffice')
    
    # Sécurité / Fallbacks selon l'OS si non trouvé dans le PATH automatique
    if not soffice_path:
        if os.name == 'nt':  # Windows
            soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
        elif os.path.exists('/Applications/LibreOffice.app/Contents/MacOS/soffice'):  # macOS
            soffice_path = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
        else:
            soffice_path = 'soffice'  # On tente la commande globale (Linux)

    # Commande magique de conversion headless de LibreOffice
    cmd = [
        soffice_path,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', output_dir,
        docx_path
    ]
    
    try:
        # Exécution de la commande système
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        
        # Détermination du chemin du fichier PDF généré (LibreOffice garde le même nom de base)
        base_name = os.path.splitext(os.path.basename(docx_path))[0]
        pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
        
        if os.path.exists(pdf_path):
            return pdf_path
        else:
            raise Exception(f"Le fichier PDF n'a pas été généré. Sortie erreur : {result.stderr}")
            
    except subprocess.CalledProcessError as e:
        raise Exception(f"Erreur lors de la conversion LibreOffice : {e.stderr or e.stdout}")
    except FileNotFoundError:
        raise Exception(
            "LibreOffice n'est pas installé ou n'est pas accessible dans le PATH du système. "
            "Exécutez 'sudo apt-get install libreoffice' sur votre serveur Linux."
        )