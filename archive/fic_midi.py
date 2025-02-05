import openai
from mido import MidiFile, MidiTrack, Message

# Clé API OpenAI
openai.api_key = 'sk-FKbMr-l2TV2IkUED7ENFi9yF_wd10p43cUMMmOsF7tT3BlbkFJ36_w8QhV73Y27slXXTzw3dlZ8grxhxsBTRx1D2c_0A'

# Fonction pour générer une mélodie à partir d'une description textuelle
def generer_melodie(description):
    # Appel à l'API OpenAI pour générer la séquence de notes
    response = openai.Completion.create(
        engine="whisper-1",
        prompt=f"Génère une séquence de notes pour une mélodie {description}. Utilise des notes standards (A, B, C, D, E, F, G) avec des octaves et des durées.",
        max_tokens=100
    )
    
    # Récupérer la réponse générée
    notes = response.choices[0].text.strip()
    return notes

# Fonction pour créer un fichier MIDI à partir des notes générées
def creer_fichier_midi(notes, fichier_sortie='melodie.mid'):
    # Créer un nouvel objet MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Dictionnaire pour convertir les notes en codes MIDI
    note_to_midi = {
        'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65,
        'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71
    }
    
    # Découper les notes générées et les ajouter au fichier MIDI
    for note in notes.split(','):
        note = note.strip()
        if note and note[0] in note_to_midi:
            midi_note = note_to_midi[note[0]]  # Convertir la note en code MIDI
            track.append(Message('note_on', note=midi_note, velocity=64, time=200))
            track.append(Message('note_off', note=midi_note, velocity=64, time=400))
    
    # Sauvegarder le fichier MIDI
    mid.save(fichier_sortie)
    print(f"Mélodie sauvegardée dans {fichier_sortie}")

# Exemple d'utilisation
description = "une mélodie joyeuse en Do majeur, lente et relaxante"
notes_generes = generer_melodie(description)
print(f"Notes générées : {notes_generes}")

# Créer un fichier MIDI avec la mélodie générée
creer_fichier_midi(notes_generes)