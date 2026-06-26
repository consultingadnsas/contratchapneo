import docx
import re

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