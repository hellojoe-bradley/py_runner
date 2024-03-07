import pygame
import os
import random
import time

pygame.init()

#GLOBAL CONSTANTS:
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font("px_sprites/font/Chava-Regular.ttf", 24)
clock = pygame.time.Clock()
game_running = 0
game_over = 1

#LOAD IMAGES

# For sprite animation, I'm using f string to generate a sequence to iterate through filenames,
# i.e. i = 1 => run1.png, so it moves through rin{i}.png from 1 to 7
run = [pygame.image.load(os.path.join('px_sprites/scaled_sprites', f'run{i}.png')) for i in range(1, 7)]
jump = pygame.image.load(os.path.join('px_sprites/scaled_sprites', 'jump.png'))
duck = pygame.image.load(os.path.join('px_sprites/scaled_sprites', 'duck_static.png'))
#duck = [pygame.image.load(os.path.join('px_sprites/scaled_sprites', f'duck{i}.png')) for i in range(1, 7)]
track = pygame.image.load(os.path.join('px_sprites/scaled_sprites', 'track.png'))
ground_enemy = [pygame.image.load(os.path.join('px_sprites/scaled_sprites', f'ground_enemy{i}.png')) for i in range(1, 4)]
sky_enemy = [pygame.image.load(os.path.join('px_sprites/scaled_sprites', f'sky_enemy{i}.png')) for i in range(1, 6)]
point = pygame.image.load(os.path.join('px_sprites/scaled_sprites', 'point.png'))


class Runner:
    x_pos = 80
    y_pos = 350
    is_jumping = False
    is_ducking = False
    duck_frame_number = 0
    run_frame_number = 0
    jump_vel = 15
    def __init__(self, run_images, jump_image, duck_images):
        self.run_images = run
        self.jump_image = jump
        #self.duck_images = duck
        self.duck_image = duck

    def draw(self, screen):
        #if is_jumping is true, change y_pos by subtracking the value of jump_vel * 4, and decrement 
        # the value of jump_vel by 1 for every iteration (while is_jumping is true). if the y_pos meets  
        # or exceeds the location of the track (350px), it sets is_jumping to false and reassigns 
        # the y_pos to 350 and jump_vel to 0 then, lastly, it blits the jump_image to the screen.
        if self.is_jumping:
            self.y_pos -= self.jump_vel * 4
            self.jump_vel -= 1.25
            if self.y_pos >= 350:
                self.is_jumping = False
                self.y_pos = 350
                self.jump_vel = 0
            screen.blit(self.jump_image, (self.x_pos, self.y_pos))
        # if is_ducking is true,
        elif self.is_ducking:
            screen.blit(self.duck_image, (self.x_pos, self.y_pos))\
        #if not jumping or ducking, the code runs the running animation
        else:
            screen.blit(self.run_images[self.run_frame_number], (self.x_pos, self.y_pos))
            self.run_frame_number += 1
            if self.run_frame_number >= 6:
                self.run_frame_number = 0
    
    #this function checks if the player is currently jumping, if not
    #it sets is_jumping to true and sets jump_vel equal to 5
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_vel = 5

    #checks if player is ducking, if not, is_ducking = True
    def duck(self):
        if not self.is_ducking:
            self.is_ducking = True

#function to draw the ground enemy type
#screen is the surface that the sprite will be drawn on
#ge_frame_number is the current image in the array being displayed
#ground_enemy_images is a list of surface objects that represent the images in the array
#x and y pos are self explanatory
#ground_enemy_frame_rate was made to animate the sprite independently from other sprites
#last_update_time is the time in milliseconds since the last frame update
def draw_ground_enemy(screen, ge_frame_number, ground_enemy_images, enemy_x_pos, enemy_y_pos, ground_enemy_frame_rate, last_update_time_ground):
    #time_since_last_update is used to  ensure that enough time has passed according to the individual frame rate
    #it calculates this using get_ticks to retrieve the current time in milliseconds and subract last_update_time from it
    time_since_last_update = pygame.time.get_ticks() - last_update_time_ground
    
    #if enough time has passes (i.e if statement condition), ge_frame_number moves to the next frame
    #and last_update_time is updated with the most recent time stamp
    if time_since_last_update >= 1000 / ground_enemy_frame_rate:
        # Move to the next frame
        ge_frame_number = (ge_frame_number + 1) % len(ground_enemy_images)
        # Update the last update time
        last_update_time_ground = pygame.time.get_ticks()
    
    # Move the enemy from right to left
    if enemy_x_pos >= -10:
        enemy_x_pos -= 24
    else:
        # Relocate the enemy to a random position to the right of the screen width once it goes off-screen
        enemy_x_pos = screen_width + random.randint(100, 2000)
    
    # Draw the current frame of the ground_enemy sprite
    screen.blit(ground_enemy_images[ge_frame_number], (enemy_x_pos, enemy_y_pos))
    
    # Return updated values for use in the main loop
    return ge_frame_number, last_update_time_ground, enemy_x_pos

#same logic as ground enemy
def draw_sky_enemy(screen, se_frame_number, sky_enemy_images, sky_enemy_x_pos, enemy_y_pos, sky_enemy_frame_rate, last_update_time_sky):
    time_since_last_update = pygame.time.get_ticks() - last_update_time_sky
    if time_since_last_update >= 1000 / sky_enemy_frame_rate:
        se_frame_number = (se_frame_number + 1) % len(sky_enemy_images)
        last_update_time_sky = pygame.time.get_ticks()
    if sky_enemy_x_pos >= -10:
        sky_enemy_x_pos -= 24
    else:
        sky_enemy_x_pos = screen_width + random.randint(100, 5000)
    screen.blit(sky_enemy_images[se_frame_number], (sky_enemy_x_pos, enemy_y_pos))
    return se_frame_number, last_update_time_sky, sky_enemy_x_pos

def run_game():
    runner = Runner(run, jump, duck)
    track_x_pos = 0
    track_y_pos = 387
    frame_rate = 24
    enemy_x_pos_ground = screen_width + 100
    enemy_y_pos_ground = 350
    ge_frame_number = 0
    ground_enemy_frame_rate = 8
    enemy_x_pos_sky = screen_width + random.randint(500, 1000)
    enemy_y_pos_sky = 330
    se_frame_number = 0
    sky_enemy_frame_rate = frame_rate
    last_update_time_sky = pygame.time.get_ticks()
    points = 0
    point_x_pos = screen_width + random.randint(100, 1000)
    point_y_pos = 300
    you_win_message = font.render("You Win!", True, (0,0,0))
    game_over_message = font.render("Game Over :(", True, (0,0,0))

    def track_scroll():
        nonlocal track_x_pos
        image_width = track.get_width()
        screen.blit(track,(track_x_pos, track_y_pos))
        screen.blit(track, (image_width + track_x_pos, track_y_pos))
        track_x_pos -= frame_rate
        if track_x_pos <= -image_width:
            track_x_pos = 0

    def point_scroll():
        nonlocal point_x_pos
        screen.blit(point,(point_x_pos, point_y_pos))
        point_x_pos -= frame_rate
        if point_x_pos <= -100:
            point_x_pos = screen_width + random.randint(100, 1000)
    #MAIN LOOP
    running = True
    #create flag to check if player is ducking or not (down key is pressed)
    is_ducking = False
    last_update_time_ground = pygame.time.get_ticks()
    #initialize collision_frame_count to 0 outside the main loop to avoid it being 
    #reset to 0 every frame that the collision is occuring.
    collision_frame_count = 0 
    pt_collision_frame_count = 0

    while running:
        #loop over all events 
        for event in pygame.event.get():
            #check if window's x button was pressed, if so, quit
            if event.type == pygame.QUIT:
                running = False
            #both nest3ed if statements check if either up key or down key are being pressed
            #if so, it calls either coresponding function
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    runner.jump()
                if event.key == pygame.K_DOWN:
                    runner.duck()
                    #sets is ducking to true, meaning the key is being pressed
                    is_ducking = True
            #if KEYUP event happens, it means the key has been released, setting is_ducking 
            #to false, and stops the duck animation
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_ducking = False
                    #by settinfg runner.is_ducking to False here, it restarts the ducking animation immediately
                    #rather than waiting until the animation is complete
                    runner.is_ducking = False

        screen.fill((255,255,255))
        track_scroll()
        point_scroll()

        #this line uses the updated values from the last execution of the function
        ge_frame_number, last_update_time_ground, enemy_x_pos_ground = draw_ground_enemy(screen, 
                                                                                ge_frame_number, 
                                                                                ground_enemy, 
                                                                                enemy_x_pos_ground, 
                                                                                enemy_y_pos_ground, 
                                                                                ground_enemy_frame_rate, 
                                                                                last_update_time_ground)
        
        # Update and draw the sky enemy
        se_frame_number, last_update_time_sky, enemy_x_pos_sky = draw_sky_enemy(screen, 
                                                                         se_frame_number, 
                                                                         sky_enemy, 
                                                                         enemy_x_pos_sky, 
                                                                         enemy_y_pos_sky, 
                                                                         sky_enemy_frame_rate, 
                                                                         last_update_time_sky)
        
        
        #if the distance between the enemies is less than 100 pixels, increase the x position
        # of the sky enemy by a random integer between the two kiven values
        if abs(enemy_x_pos_ground - enemy_x_pos_sky) < 200:
        # If they are too close, adjust the x position of one of the enemies
        # For example, you can randomly move one of them to the right
            enemy_x_pos_sky += random.randint(100, 300)

        if is_ducking:
            runner.duck()
        runner.draw(screen)

        #create player mask with statements to specify which sprite the mask is made from
        runner_mask = pygame.mask.from_surface(runner.run_images[0])
        if runner.is_jumping and not runner.is_ducking:
            runner_mask = pygame.mask.from_surface(runner.jump_image)
        elif runner.is_ducking and not runner.is_jumping:
            runner_mask = pygame.mask.from_surface(runner.duck_image)
        else:
            runner_mask = pygame.mask.from_surface(runner.run_images[runner.run_frame_number])
        mask_image = runner_mask.to_surface()

        #create enemy masks
        ground_enemy_mask = pygame.mask.from_surface(ground_enemy[ge_frame_number])
        sky_enemy_mask = pygame.mask.from_surface(sky_enemy[se_frame_number])
        point_mask = pygame.mask.from_surface(point)      

        #check if player mask is colliding with either enemy mask
        if runner_mask.overlap(ground_enemy_mask, (enemy_x_pos_ground - runner.x_pos, enemy_y_pos_ground - runner.y_pos)) or runner_mask.overlap(sky_enemy_mask, (enemy_x_pos_sky - runner.x_pos, enemy_y_pos_sky - runner.y_pos)):
            #make sure that no collision frames have happened before executing logid
            if collision_frame_count == 0:
                #decrement points by 1, and set collision_frame_count to 1 to avoid executing the logic again 
                #for every frame that the masks are overlapping 
                print("collision")
                points -= 1
                collision_frame_count = 1
        else:
            #after the collision logic executes, reset collision_frame_count so that the logic can repeat 
            #again for future collisions
            collision_frame_count = 0

        if runner_mask.overlap(point_mask, (point_x_pos - runner.x_pos, point_y_pos - runner.y_pos)):
            if pt_collision_frame_count == 0:
                #decrement points by 1, and set collision_frame_count to 1 to avoid executing the logic again 
                #for every frame that the masks are overlapping 
                print("point")
                points += 1
                point_x_pos = -1000
                pt_collision_frame_count = 1
        else:
            #after the collision logic executes, reset collision_frame_count so that the logic can repeat 
            #again for future collisions
            pt_collision_frame_count = 0

        #update and display score
        score_text = font.render(str(points), True, (0,0,0))
        screen.blit(score_text, (525,10))
        if points >= 10:
            screen.fill((255,255,255))
            screen.blit(you_win_message, (475, 300))
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
        if points < 0:
            screen.fill((255,255,255))
            screen.blit(game_over_message, (475, 300))
            pygame.display.update()
            time.sleep(5)
            pygame.quit()

        pygame.display.update()
        clock.tick(frame_rate)

    pygame.quit()

run_game()
