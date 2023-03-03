import pygame
import utils
import models



class SpiceStroids:

    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800,600))
        self.background = utils.load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.bullets = []
        self.spaceship = models.Spaceship((400, 300), self.bullets.append)
        self.asteroids = []
        
        for _ in range(6):
            foundPos = False
            while not foundPos:
                position = utils.get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.getPosition()) 
                    > self.MIN_ASTEROID_DISTANCE
                    ):

                    foundPos = True
                    
            
            self.asteroids.append(models.Asteroid(position))


        pygame.key.set_repeat(20, 20)
        pygame.mixer.music.load("assets/bgm/Attack on Titan Theme (Guren no Yumiya) - Violin - Taylor Davis.ogg")
        #pygame.mixer.music.play(-1)
        
            

    
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("SpiceStroids")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

            elif event.type == pygame.KEYDOWN and self.spaceship != None:
                if event.key == pygame.K_LALT:
                    self.spaceship.boost(self.screen)
                
                elif event.key == pygame.K_SPACE:
                    self.spaceship.shoot()


            is_key_pressed = pygame.key.get_pressed()

            if self.spaceship != None:
                if is_key_pressed[pygame.K_RIGHT]:
                    self.spaceship.rotate(clockwise = True)

                if is_key_pressed[pygame.K_LEFT]:
                    self.spaceship.rotate(clockwise = False)

                if is_key_pressed[pygame.K_UP]:
                    self.spaceship.accelerate()

             
    def _process_game_logic(self):
        for game_object in self._get_game_objects():
           game_object.move(self.screen)


        if self.spaceship != None:
            i = 0
            collided = False
            while (i < len(self.asteroids) and not collided):
                asteroid = self.asteroids[i]
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    collided = True
                i+=1


        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.getPosition()):
                self.bullets.remove(bullet)

            else:
                i = 0
                collided = False
                while i < len(self.asteroids) and not collided:
                    asteroid = self.asteroids[i]
                    if bullet.collides_with(asteroid):
                        self.asteroids.remove(asteroid)
                        self.bullets.remove(bullet)
                        collided = True
                    i += 1


                    

            



        
        #print("Collides:", self.spaceship.collides_with(self.asteroid))

    def _draw(self):
        self.screen.blit(self.background, (0,0))
        for game_object in self._get_game_objects():
           game_object.draw(self.screen)
       
        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship != None:
            game_objects.append(self.spaceship)

        return game_objects

        
       




    
    




