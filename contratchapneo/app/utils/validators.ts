// utils.ts

// On accepte n'importe quel objet avec des clés en string (le formulaire)
export function validateForm(fields: Record<string, any>) {
    let isValid = true;
    
    // On crée un objet d'erreurs dynamique
    const errors: Record<string, string> = {};

    // On boucle sur chaque champ passé au formulaire
    for (const key in fields) {
        const value = fields[key];
        
        // On initialise l'erreur pour ce champ à vide
        errors[key] = "";

        // 1. Règle générale : Si c'est du texte et que c'est vide
        if (typeof value === 'string' && value.trim() === "") {
            errors[key] = "Ce champ est requis.";
            isValid = false;
            continue; // On passe au champ suivant pour ne pas écraser cette erreur
        }

        // 2. Règle spécifique : Si la clé contient "email" (ex: email, user_email, guestEmail)
        if (key.toLowerCase().includes('email') && typeof value === 'string') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                errors[key] = "Veuillez entrer une adresse email valide.";
                isValid = false;
            }
        }

        // 3. Règle spécifique : Si la clé contient "password" ou "mot_de_passe"
        if ((key.toLowerCase().includes('password') || key.toLowerCase().includes('mot_de_passe')) && typeof value === 'string') {
            if (value.length < 8) {
                errors[key] = "Doit contenir au moins 8 caractères.";
                isValid = false;
            }
        }
    }

    // On retourne le statut global et l'objet contenant toutes les erreurs générées
    return { isValid, errors };
}