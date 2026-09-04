import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// Dictionnaire des intentions et mots-clés
const intents = [
    {
        id: 'salutation',
        keywords: ['bonjour', 'salut', 'coucou', 'hello', ],
        messages: [
            "Bonjour ! 👋",
            "Je suis l'assistant virtuel de ContratChapNeo.",
            "Que puis-je faire pour vous aujourd'hui ?"
        ]
    },
    {
        id: 'contrat',
        keywords: ['contrat', 'modele', 'rediger', 'document', 'ohada', 'pdf', 'word', 'cdd', 'cdi'],
        messages: [
            "Je vois que vous cherchez un modèle de document.",
            "Nous avons toute une bibliothèque de contrats OHADA prêts à l'emploi.",
            "Vous pouvez les consulter dans notre section 'Contrats'."
        ],
        action: 'redirect_contrats' // Redirection optionnelle
    },
    {
        id: 'simulateur',
        keywords: ['calcul', 'simulateur', 'droit', 'licenciement', 'demission', 'indemnite', 'salaire'],
        messages: [
            "Vous souhaitez faire une simulation de vos droits de rupture ?",
            "Je vous redirige vers notre simulateur conforme au Code du Travail."
        ],
        action: 'redirect_simulateur'
    },
    {
        id: 'prix',
        keywords: ['prix', 'tarif', 'pack', 'abonnement', 'combien', 'payant'],
        messages: [
            "Nos modèles sont accessibles via différents packs.",
            "Laissez-moi vous rediriger vers notre page de tarifs."
        ],
        action: 'redirect_packs'
    },
    {
    id: 'assistance_appel',
    keywords: ['aide', 'assistance', 'appel', 'joindre', 'telephone', 'support', 'humain', 'probleme', 'centre'],
    messages: [
        "Vous souhaitez échanger de vive voix avec notre équipe ? 📞",
        "Notre centre d'appel est là pour vous accompagner.",
        "Je vous redirige vers nos coordonnées."
    ],
    action: 'redirect_contact'
    },
    {
        id: 'consultation_pro',
        keywords: ['pro', 'professionnel', 'expert', 'avocat', 'juriste', 'consultation', 'conseil', 'cabinet', 'aviser'],
        messages: [
            "Votre situation nécessite une expertise juridique approfondie ? ⚖️",
            "Nos experts en droit OHADA sont à votre disposition pour une consultation.",
            "Laissez-moi vous guider vers notre espace professionnel."
        ],
        action: 'redirect_pro'
    },
    {
        id: 'info_pack',
        keywords: ['info', 'information', 'detail', 'savoir', 'voir', 'prix', 'tarif', 'combien', 'offre', 'decouvrir'],
        messages: [
            "Vous souhaitez en savoir plus sur nos offres ? 📦",
            "Nous proposons plusieurs packs économiques selon vos besoins.",
            "Je vous emmène directement à la section de nos offres."
        ],
        action: 'redirect_info_pack'
    },
    {
        id: 'achat_pack',
        keywords: ['acheter', 'obtenir', 'souscrire', 'prendre', 'payer', 'achat', 'commander', 'panier'],
        messages: [
            "Excellente décision ! 🎉",
            "Pour souscrire à un pack, vous devez d'abord vous identifier.",
            "Je vous redirige vers la page de connexion."
        ],
        action: 'redirect_achat_pack'
    }
];

const fallbackNode = {
    messages: [
        "Je ne suis pas sûr d'avoir bien compris votre demande. 🤔",
        "Pourriez-vous reformuler ?",
        "Vous pouvez me parler de 'contrats', de 'calcul de droits' ou de nos 'packs'."
    ]
};

const levenshtein = (a: string, b: string): number => {
    const matrix = [];
    for (let i = 0; i <= b.length; i++) matrix[i] = [i];
    for (let j = 0; j <= a.length; j++) matrix[0][j] = j;

    for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
            if (b.charAt(i - 1) === a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1, // substitution
                    matrix[i][j - 1] + 1,     // insertion
                    matrix[i - 1][j] + 1      // suppression
                );
            }
        }
    }
    return matrix[b.length][a.length];
};

export const useChatStore = defineStore('chat', () => {
    const router = useRouter();
    
    const isOpen = ref(false);
    const isTyping = ref(false);
    const messages = ref<{ sender: 'bot' | 'user', text: string }[]>([]);

    const toggleChat = () => {
        isOpen.value = !isOpen.value;
        if (isOpen.value && messages.value.length === 0) {
            playMessagesSequentially(intents.find(i => i.id === 'salutation')!.messages);
        }
    };

    // Nettoie le texte (minuscules, sans accents) pour faciliter la recherche
    const normalizeText = (text: string) => {
        return text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    };

    // Le moteur de recherche de mots-clés
    const analyzeInput = (userText: string) => {
        messages.value.push({ sender: 'user', text: userText });
        
        const normalizedPhrase = normalizeText(userText);
        const userWords = normalizedPhrase.split(/[\s,.'’]+/); // Découpe en mots
        
        let matchedIntent = null;

        for (const intent of intents) {
            let isMatch = false;

            for (const keyword of intent.keywords) {
                // 1. Vérification exacte de la phrase (utile si le mot-clé contient un espace)
                if (normalizedPhrase.includes(keyword)) {
                    isMatch = true;
                    break;
                }

                // 2. Vérification mot par mot avec tolérance aux fautes de frappe
                for (const word of userWords) {
                    const diff = levenshtein(word, keyword);
                    
                    // Règle de tolérance intelligente :
                    // - Mots longs (>5 lettres) : 2 fautes tolérées maximum
                    // - Mots moyens (4-5 lettres) : 1 faute tolérée
                    // - Petits mots (<4 lettres) : correspondance exacte exigée
                    if (
                        (keyword.length > 5 && diff <= 2) || 
                        (keyword.length > 3 && keyword.length <= 5 && diff <= 1) ||
                        (keyword.length <= 3 && diff === 0)
                    ) {
                        isMatch = true;
                        break;
                    }
                }
                if (isMatch) break;
            }

            if (isMatch) {
                matchedIntent = intent;
                break;
            }
        }

        if (matchedIntent) {
            playMessagesSequentially(matchedIntent.messages, matchedIntent.action);
        } else {
            playMessagesSequentially(fallbackNode.messages);
        }
    };

    const playMessagesSequentially = async (msgs: string[], action?: string) => {
        for (let i = 0; i < msgs.length; i++) {
            isTyping.value = true;
            
            const textContent = msgs[i];
            const typingDuration = 400 + (textContent.length * 25);
            
            await new Promise(resolve => setTimeout(resolve, typingDuration));
            
            isTyping.value = false;
            messages.value.push({ sender: 'bot', text: textContent });
            
            if (i < msgs.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 300));
            }
        }

        // Exécuter l'action après la fin des messages
        if (action) {
            setTimeout(() => executeAction(action), 1000);
        }
    };

    const executeAction = (action: string) => {
        if (action === 'redirect_simulateur') router.push('/simulateur');
        else if (action === 'redirect_contrats') router.push('/contractBank');
        else if (action === 'redirect_contact') router.push('/services'); 
        else if (action === 'redirect_pro') router.push('/pro'); 
        
        // NOUVEAU : Redirection vers la page de connexion pour achat
        else if (action === 'redirect_achat_pack') {
            router.push('/auth/login');
        }
        
        // NOUVEAU : Redirection vers /contractBank et scroll vers les packs
        else if (action === 'redirect_info_pack') {
            router.push('/contractBank').then(() => {
                // On attend 500ms pour laisser le temps au DOM de se construire
                setTimeout(() => {
                    // On cherche la section des packs grâce à sa classe CSS
                    const packSection = document.querySelector('.packages-section');
                    if (packSection) {
                        packSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    } else {
                        // Fallback de sécurité : on descend de 800 pixels si la classe n'est pas trouvée
                        window.scrollBy({ top: 800, behavior: 'smooth' });
                    }
                }, 500);
            });
        }
    };

    return { isOpen, isTyping, messages, toggleChat, analyzeInput };
});