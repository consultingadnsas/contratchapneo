import re
import docx

def extract_tags_from_docx(file_path):

    """
        Ouvre un document DOCX, lit le texte et extrait toutes les balises
        au format {{ nom _variable }}
    """

    try:
        # 1. Ouvrir le document
        
        doc = docx.Document(file_path)
        full_text = []

        # 2. Extraire tout le texte des paragraphes

        for para in doc.paragraphs:
            full_text.append(para.text)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    full_text.append(cell.text)

        text = '\n'.join(full_text)

        # 3. Trouver toutes les balises avec une expression régulière (Regex)
        # Ici on cherche tout ce qui est entre {{ et }}, en ignorant les espaces autour
        tags = re.findall(r'\{\{\s*(.*?)\s*\}\}', text)

        # 4. Retourner une liste unique (set) pour éviter les doublons
        # (Si {{ nom}} apparaît 3 fois, on ne le veut qu'une seule fois)

        return list(set(tags))
    
    except Exception as e:

        print(f"Erreur lors de la lecture du fichier : {e}")
        return []

