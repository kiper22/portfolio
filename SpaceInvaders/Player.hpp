// Player.hpp

#ifndef PLAYER_HPP
#define PLAYER_HPP

#include <SFML/Graphics.hpp>
#include <cstdlib>
#include <iostream>
#include <memory>
#include "settings.hpp"
#include "Ship.hpp"
#include "Ammo.hpp"

class PlayerShip : public Ship {
public:
    PlayerShip(const sf::Vector2f& position, const std::string& texturePath) : Ship(position, texturePath) {
        shooting_clock.restart();
    }

    ~PlayerShip() {}

    void handleInput() {
        float movementSpeed = Settings::PLAYER_SPEED;
        float shootingInterval = Settings::PLAYER_SHOOTING_TIME;

        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left)) {
            sprite.move(-movementSpeed, 0);
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right)) {
            sprite.move(movementSpeed, 0);
        }

        sf::Vector2f new_position = sprite.getPosition();
        if (new_position.x < 0) {
            new_position.x = 0;
        } else if (new_position.x > Settings::WINDOW_WIDTH - sprite.getGlobalBounds().width) {
            new_position.x = Settings::WINDOW_WIDTH - sprite.getGlobalBounds().width;
        }

        sprite.setPosition(new_position);

        if (shooting_clock.getElapsedTime().asSeconds() > shootingInterval) {
            player_ammos.push_back(std::make_unique<Ammo>(getGunPosition(), "sprites/ammo.png", Settings::PLAYER_AMMO_SPEED));

            shooting_clock.restart();
        }

    }

    void update() {
        for (auto it = player_ammos.begin(); it != player_ammos.end();) {
            (*it)->update();
            if ((*it)->isOutOfBounds()) {
                it = player_ammos.erase(it);
            } else {
                ++it;
            }
        }
    }

    sf::Vector2f getPosition() const {
        return sprite.getPosition();
    }

    std::vector<std::unique_ptr<Ammo>>& getPlayerAmmos() {
        return player_ammos;
    }

    void loseLife() {
        lives--;
    }

    int getLives() const {
        return lives;
    }

    void updateTexture() {
        if (lives ==2) {
            std::string updatedTexturePath = "sprites/player_2.png";
            setTexture(updatedTexturePath);
        }
        else if (lives==1) {
            std::string updatedTexturePath = "sprites/player_3.png";
            setTexture(updatedTexturePath);
        }
    }

private:
    sf::Clock shooting_clock;
    std::vector<std::unique_ptr<Ammo>> player_ammos;
    int lives = Settings::PLAYER_LIVES_START;
};
#endif // PLAYER_HPP
