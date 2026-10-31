"""Module de gestion du vocabulaire du modèle pour le décodage contraint."""

import json
from pathlib import Path


def _byte_decoder() -> dict[str, int]:
    """Inverse of the GPT-2/Qwen byte-level mapping (unicode char -> raw byte)."""
    codes = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(0xA1, 0xAC + 1))
        + list(range(0xAE, 0xFF + 1))
    )
    chars = codes[:]
    extra = 0
    for byte in range(256):
        if byte not in codes:
            codes.append(byte)
            chars.append(256 + extra)
            extra += 1
    return {chr(c): b for b, c in zip(codes, chars)}


_BYTE_DECODER = _byte_decoder()


def _decode_token(raw_token: str) -> str:
    """Turn a raw vocab entry (e.g. 'Ġworld', 'Ã©') into its real text (' world', 'é')."""
    try:
        data = bytes(_BYTE_DECODER[c] for c in raw_token)
    except KeyError:  # special / added tokens that are not byte-level encoded
        return raw_token
    return data.decode("utf-8", errors="replace")


class Vocabulary:
    """Gestionnaire du vocabulaire permettant le mapping entre tokens et IDs."""

    def __init__(self, vocab_path: str | Path) -> None:
        """Charge et pré-traite le fichier de vocabulaire JSON.

        Args:
            vocab_path: Chemin vers le fichier vocab.json.
        """
        path = Path(vocab_path)
        if not path.is_file():
            raise FileNotFoundError(f"Fichier de vocabulaire introuvable : {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                self.token_to_id: dict[str, int] = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Erreur de lecture du vocabulaire JSON : {exc}") from exc

        # Dictionnaire ID -> Texte nettoyé (décodage byte-level unique au chargement :
        # "Ġ" -> espace, "Ċ" -> saut de ligne, "Ã©" -> "é", etc.)
        self.id_to_token: dict[int, str] = {
            token_id: _decode_token(raw_token)
            for raw_token, token_id in self.token_to_id.items()
        }

    @property
    def texts(self) -> dict[int, str]:
        """Retourne le mapping complet des IDs vers les textes nettoyés."""
        return self.id_to_token

    @property
    def _token_to_id(self) -> dict[str, int]:
        return self.token_to_id

    @property
    def _id_to_clean_text(self) -> dict[int, str]:
        return self.id_to_token

    def get_clean_text(self, token_id: int) -> str:
        """Retourne le texte nettoyé correspondant à un ID de token."""
        return self.id_to_token.get(token_id, "")

    def get_id(self, token_str: str) -> int | None:
        """Retourne l'ID d'un token brut ou nettoyé s'il existe."""
        return self.token_to_id.get(token_str)

    def get_token_ids_matching(self, allowed_strings: set[str]) -> list[int]:
        """Retourne les IDs de tokens correspondant exactement à un texte autorisé."""
        return [
            token_id
            for token_id, text in self.id_to_token.items()
            if text in allowed_strings
        ]

    def get_token_ids_starting_with(self, prefix: str) -> list[int]:
        """Retourne les IDs de tokens qui débutent par un préfixe donné."""
        return [
            token_id
            for token_id, text in self.id_to_token.items()
            if text.startswith(prefix)
        ]


# Alias pour rétro-compatibilité avec les anciens imports
TokenVocabulary = Vocabulary
