from settings import *

"""
Simplest way of loading external images
"""
white_pawn = pygame.image.load(path.join(assets_dir,"wp.png")).convert_alpha()
black_pawn = pygame.image.load(path.join(assets_dir,"bp.png")).convert_alpha()

white_rock = pygame.image.load(path.join(assets_dir,"wR.png")).convert_alpha()
black_rock = pygame.image.load(path.join(assets_dir,"bR.png")).convert_alpha()

white_knight = pygame.image.load(path.join(assets_dir,"wN.png")).convert_alpha()
black_knight = pygame.image.load(path.join(assets_dir,"bN.png")).convert_alpha()

white_bishop = pygame.image.load(path.join(assets_dir,"wB.png")).convert_alpha()
black_bishop = pygame.image.load(path.join(assets_dir,"bB.png")).convert_alpha()

white_queen = pygame.image.load(path.join(assets_dir,"wQ.png")).convert_alpha()
black_queen = pygame.image.load(path.join(assets_dir,"bQ.png")).convert_alpha()

white_king = pygame.image.load(path.join(assets_dir,"wK.png")).convert_alpha()
black_king = pygame.image.load(path.join(assets_dir,"bK.png")).convert_alpha()

#-- Sounds
pick = mixer.Sound(path.join(assets_dir,"pick.ogg"))
engine_tick = mixer.Sound(path.join(assets_dir,"tick_002.ogg"))
