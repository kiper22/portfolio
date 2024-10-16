#pragma once

#include <SFML/Graphics.hpp>
#include <ctime>
#include <memory>
#include "Settings.hpp"
#include "Ship.hpp"
#include "Player.hpp"
#include "EnemyShip.hpp"
#include "Ammo.hpp"


class Window {
public:
    Window() : window(sf::VideoMode(Settings::WINDOW_WIDTH, Settings::WINDOW_HEIGHT), "SFML Window"),
               playerShip(sf::Vector2f(Settings::SHIP_STARTING_X, Settings::SHIP_STARTING_Y), "sprites/player_1.png") {
            wave_clock.restart(); 
            player_ammo_clock.restart();
            initialize_enemies();
    }

    void run() {
        sf::Clock frameClock;

        while (window.isOpen()) {
            handleEvents();
            
            sf::Time elapsed = frameClock.restart();

            update();
            render();

            sf::Time sleepTime = sf::milliseconds(5) - elapsed; 
            if (sleepTime > sf::Time::Zero) {
                sf::sleep(sleepTime);
            }
        }
    }

private:
    int killed_enemies = 0;
    sf::Clock wave_clock;
    sf::Clock player_ammo_clock;
    sf::RenderWindow window;
    PlayerShip playerShip;
    std::unique_ptr<EnemyShip> enemyPtr;
    std::vector<std::unique_ptr<EnemyShip>> enemyShips;
    std::vector<std::unique_ptr<Ammo>> playerAmmos;
    std::vector<std::unique_ptr<Ammo>> allEnemyAmmos;

    void handleEvents() {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
        }
        playerShip.handleInput();

    }

    void handle_game_over() {
        std::cout << "Game Over! Score: " << killed_enemies << std::endl;
        window.close();
    }

    void initialize_enemies() {
        std::srand(static_cast<unsigned>(std::time(0)));

        for (int i = 0; i < Settings::NUM_ENEMY_SHIPS; ++i) {
            float xPosition = i * (Settings::WINDOW_WIDTH / Settings::NUM_ENEMY_SHIPS);
            float yPosition = 0;

            int enemyType = std::rand() % 4;

            switch (enemyType) {
                case 0:
                    enemyPtr = std::make_unique<GreenEnemy>(sf::Vector2f(xPosition, yPosition), &playerShip); //, &playerShip
                    break;
                case 1:
                    enemyPtr = std::make_unique<RedEnemy>(sf::Vector2f(xPosition, yPosition), &playerShip);
                    break;
                case 2:
                    enemyPtr = std::make_unique<YellowEnemy>(sf::Vector2f(xPosition, yPosition), &playerShip);
                    break;
                case 3:
                    enemyPtr = std::make_unique<PurpleEnemy>(sf::Vector2f(xPosition, yPosition), &playerShip);
                    break;
            }
            enemyShips.push_back(std::move(enemyPtr));
        }
    }

    void handle_collisions() {
        for (auto itEnemy = enemyShips.begin(); itEnemy != enemyShips.end();) {
            for (auto itAmmo = playerShip.getPlayerAmmos().begin(); itAmmo != playerShip.getPlayerAmmos().end();) {
                if ((*itEnemy)->getGlobalBounds().intersects((*itAmmo)->getGlobalBounds())) {
                    itEnemy = enemyShips.erase(itEnemy);
                    itAmmo = playerShip.getPlayerAmmos().erase(itAmmo);
                    killed_enemies++;
                    std::cout << "Collision detected! Killed enemies: " << killed_enemies << std::endl;  // Komunikat diagnostyczny
                } else {
                    ++itAmmo;
                }
            }

            if (itEnemy != enemyShips.end()) {
                ++itEnemy;
            }
        }
    }

    void update_enemies() {
        for (auto it = enemyShips.begin(); it != enemyShips.end();) {
            (*it)->update(&playerShip);

            for (auto& ammo : (*it)->getEnemyAmmos()) {
                allEnemyAmmos.push_back(std::move(ammo));
            }
            (*it)->getEnemyAmmos().clear();

            if ((*it)->getGlobalBounds().top > Settings::WINDOW_HEIGHT) {
                it = enemyShips.erase(it);
            } else {
                if (playerShip.getGlobalBounds().intersects((*it)->getGlobalBounds())) {
                    it = enemyShips.erase(it);
                    killed_enemies++;
                    handle_player_collision();
                    std::cout << "Player collided with an enemy! Killed enemies: " << killed_enemies << std::endl;
                } else {
                    ++it;
                }
            }
        }
    }

    void update_enemy_ammos() {
        for (auto it = allEnemyAmmos.begin(); it != allEnemyAmmos.end();) {

            if ((*it)->isOutOfBounds()) {
                it = allEnemyAmmos.erase(it);
            } 
            else if ((*it)->getGlobalBounds().intersects(playerShip.getGlobalBounds())) {
                it = allEnemyAmmos.erase(it);
                handle_player_collision();
                std::cout << "Player hit by enemy ammo! Killed enemies: " << killed_enemies << std::endl;
            } else {
                ++it;
            }
        }
    }

    void handle_player_collision() {
        playerShip.loseLife(); 
        std::cout << "Player lost live! Left lives:  " << playerShip.getLives() << std::endl;

        if (playerShip.getLives() <= 0) {
            handle_game_over();  
        } else {
            playerShip.updateTexture();
        }
    }

    void update() {
        playerShip.update();

        update_enemies();
        update_enemy_ammos();
        
        handle_collisions(); 

        if (wave_clock.getElapsedTime().asSeconds() > Settings::ENEMY_RESPAWN_TIME) {
            initialize_enemies();
            wave_clock.restart();
        }
        for (auto& ammo : allEnemyAmmos) {
            ammo->update();
        }

    }

    void render() {
        window.clear();
        playerShip.draw(window);

        for (const auto& enemyPtr : enemyShips) {
            enemyPtr->draw(window);
        }

        const auto& playerAmmos = playerShip.getPlayerAmmos();
        for (const auto& ammo : playerAmmos) {
            ammo->draw(window);
        }

        for (const auto& ammo : allEnemyAmmos) {
            ammo->draw(window);
        }

        window.display();
    }
};
