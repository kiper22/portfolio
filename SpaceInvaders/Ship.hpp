// Ship.hpp

#ifndef SHIP_HPP
#define SHIP_HPP

#include <SFML/Graphics.hpp>
#include <cstdlib>
#include "Settings.hpp"

class Ship {
public:
    Ship(const sf::Vector2f& position, const std::string& texturePath) : sprite(), texture() {
        if (!texture.loadFromFile(texturePath)) {
            exit(EXIT_FAILURE);
        }

        sprite.setTexture(texture);
        sprite.setPosition(position);
    }
    ~Ship() {}

    void draw(sf::RenderWindow& window) const {
        window.draw(sprite);
    }

    sf::FloatRect getGlobalBounds() const {
        return sprite.getGlobalBounds();
    }

    virtual sf::Vector2f getGunPosition() {
        sf::Vector2f gun_position = sprite.getPosition();
        gun_position.x += getGlobalBounds().width / 2.0f;
        return gun_position;
    }

    void setTexture(const std::string& texturePath) {
        if (!texture.loadFromFile(texturePath)) {
            exit(EXIT_FAILURE);
        }

        sprite.setTexture(texture);
    }

protected:
    sf::Sprite sprite;
    sf::Texture texture;
};

#endif // SHIP_HPP
