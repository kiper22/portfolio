// Ammo.hpp

#ifndef AMMO_HPP
#define AMMO_HPP

#include <SFML/Graphics.hpp>
#include "Settings.hpp"

class Ammo {
public:
    Ammo(const sf::Vector2f& position, const std::string& texturePath, const double speed) : sprite(), texture(), speed(speed) {
        if (!texture.loadFromFile(texturePath)) {
            exit(EXIT_FAILURE);
        }

        sprite.setTexture(texture);
        sprite.setPosition(position);
    }

    ~Ammo() {}

    void update() {
        sprite.move(0, speed);
    }

    void draw(sf::RenderWindow& window) const {
        window.draw(sprite);
    }

    sf::FloatRect getGlobalBounds() const {
        return sprite.getGlobalBounds();
    }

    bool isOutOfBounds() const {
        float top = sprite.getPosition().y;
        float bottom = top + sprite.getGlobalBounds().height;

        return (bottom < 0) || (top > Settings::WINDOW_HEIGHT);
    }

private:
    sf::Texture texture;
    sf::Sprite sprite;
    double speed;
};

#endif // AMMO_HPP
