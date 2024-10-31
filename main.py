import pygame
import sys
from button import Button

pygame.init()

initial_width, initial_height = 900, 600
minutes_width, minutes_height = 350, 150
hours_width, hours_height = 500, 150
current_size = (initial_width, initial_height)
screen = pygame.display.set_mode(current_size)
pygame.display.set_caption("Pomodoro Timer")

clock = pygame.time.Clock()

backdrop = pygame.image.load("assets/image.png")
white_button = pygame.image.load("assets/button.png")

font = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 120)
input_font = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 30)
timer_text = font.render("25:00", True, "white")
timer_text_rect = timer_text.get_rect(center=(initial_width/2, initial_height/2-25))

start_stop_button = Button(white_button, (initial_width/2, initial_height/2+100), 170, 60, "START", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#643bc5", "#e06666")
pomodoro_button = Button(None, (initial_width/2-225, initial_height/2-140), 120, 30, "Pomodoro", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#e06666")
short_break_button = Button(None, (initial_width/2-75, initial_height/2-140), 120, 30, "Short Break", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#e06666")
long_break_button = Button(None, (initial_width/2+75, initial_height/2-140), 120, 30, "Long Break", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#e06666")
custom_time_button = Button(None, (initial_width/2+225, initial_height/2-140), 120, 30, "Custom Time", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#e06666")

pomodoro_length = 1500 # 1500 secs / 25 mins
short_break_length = 300 # 300 secs / 5 mins
long_break_length = 900 # 900 secs / 15 mins
input_active = False
custom_time_input = ''
input_rect = pygame.Rect(initial_width / 2 + 200, initial_height / 2 - 125, 50, 30)

current_seconds = pomodoro_length
pygame.time.set_timer(pygame.USEREVENT, 1000)
started = False

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if timer_text_rect.collidepoint(event.pos) and (event.type == pygame.MOUSEBUTTONDOWN) == 1:
                if current_size == (initial_width, initial_height):
                    if(display_hours > 0):
                        current_size = (hours_width, hours_height)
                    else:
                        current_size = (minutes_width, minutes_height)
                else:
                    current_size = (initial_width, initial_height)
                screen = pygame.display.set_mode(current_size)

        if event.type == pygame.MOUSEBUTTONDOWN:

            if start_stop_button.check_for_input(pygame.mouse.get_pos()):
                if started:
                    started = False
                else:
                    started = True

            if pomodoro_button.check_for_input(pygame.mouse.get_pos()):
                current_seconds = pomodoro_length
                started = False

            if short_break_button.check_for_input(pygame.mouse.get_pos()):
                current_seconds = short_break_length
                started = False

            if long_break_button.check_for_input(pygame.mouse.get_pos()):
                current_seconds = long_break_length
                started = False

            if custom_time_button.check_for_input(pygame.mouse.get_pos()):
                input_active = True  # Activate the input field
                started = False
            
            if started:
                start_stop_button.text_input = "STOP"
                start_stop_button.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                                        start_stop_button.text_input, True, start_stop_button.base_color)
            else:
                start_stop_button.text_input = "START"
                start_stop_button.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                                        start_stop_button.text_input, True, start_stop_button.base_color)
        
        if input_active:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN: 
                     # User pressed Enter
                    try:
                        custom_time = int(custom_time_input) * 60  # Convert to seconds
                        if custom_time > 0:
                            current_seconds = custom_time
                        started = False
                        input_active = False
                    except ValueError:
                        pass  # Handle invalid input
                    custom_time_input = ''  # Reset input after processing
                elif event.key == pygame.K_BACKSPACE:
                    custom_time_input = custom_time_input[:-1]  # Remove last character
                else:
                    if len(custom_time_input) < 2:
                        custom_time_input += event.unicode  # Append new character
                        
                

        if event.type == pygame.USEREVENT and started:
            current_seconds -= 1

    screen.fill("#643bc5")
    screen.blit(backdrop, backdrop.get_rect(center=(current_size[0] / 2, current_size[1] / 2)))

    # Draw input box
    
    if input_active:
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)  # Draw border
        input_surface = input_font.render(custom_time_input, True, (255, 255, 255))
        screen.blit(input_surface, (input_rect.x + 7, input_rect.y - 2))

    start_stop_button.update(screen)
    start_stop_button.change_color(pygame.mouse.get_pos())
    pomodoro_button.update(screen)
    pomodoro_button.change_color(pygame.mouse.get_pos())
    short_break_button.update(screen)
    short_break_button.change_color(pygame.mouse.get_pos())
    long_break_button.update(screen)
    long_break_button.change_color(pygame.mouse.get_pos())
    custom_time_button.update(screen)
    custom_time_button.change_color(pygame.mouse.get_pos())

    if current_seconds >= 0:
        display_seconds = current_seconds % 60
        display_minutes = int(current_seconds / 60) % 60
        display_hours = current_seconds // 3600
    if(display_hours != 0):
        timer_text = font.render(f"{display_hours:02}:{display_minutes:02}:{display_seconds:02}", True, "white")
    else:
        timer_text = font.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")   
    timer_text_rect = timer_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(timer_text, timer_text_rect)

    pygame.display.update()