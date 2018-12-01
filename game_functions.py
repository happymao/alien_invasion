import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button
import score_board


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    ''' reponse for key donwn events '''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # create a bullet and add it into bullet's group
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    ''' if don't arrive limit, shot a bullet '''
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    ''' reponse for key up events '''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    ''' request keyboard and mouse events '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    ''' check whether mouse click play button '''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset game settings
        ai_settings.initialize_dynamic_settings()
        # cached mouse
        pygame.mouse.set_visible(False)
        # reset game data
        stats.reset_stats()
        stats.game_active = True
        # reset score board
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # empty aliens and bullets
        aliens.empty()
        bullets.empty()
        # create a group aliens, ane ship in center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    ''' update images on the screen, and goto refresh window '''
    # redraw screen each loop
    screen.fill(ai_settings.bg_color)
    # redraw all bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # show score
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # show new window
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ''' update bullet's position and delete undisplayed bullet '''
    # update bullet's position
    bullets.update()
    # delete undisplayed bullet
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # check bullet shoot at alien
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ''' reaction collision of bullet and alien '''
    # delete bullet and alien when they collide
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # check whether all of aliens are killed. if it is, create an other group aliens
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        # level augment
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    ''' calculate how many alien in a line '''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    ''' calculate how many line in a screen '''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    ''' create an alien and put in into current line '''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    ''' create a group aliens '''
    # create an alien and calculate how many alien in a line
    # space enter two aliens equal width of alien
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height * 5, alien.rect.height)
    # create a group of aliens
    for row_number in range(number_rows):
        # create a line aliens
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    ''' raction when aliens arrived edge '''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    ''' drop aliens and change their direction '''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ''' check alien arrived bottom '''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # reaction the same ship hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # check collision of ship and alien
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        # check alien arrived bottom
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ''' raction collision of ship and alien '''
    if stats.ships_left > 0:
        # ships_left -1
        stats.ships_left -= 1
        # update score board
        sb.prep_ships()
        # clean aliens and bullets
        aliens.empty()
        bullets.empty()
        # create an other group alien and a ship which is at center of bottom of screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # pause
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


# check high score
def check_high_score(stats, sb):
    ''' check whether high score is producted '''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
