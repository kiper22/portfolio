// EnemyShip.hpp

#ifndef ENEMY_SHIP_HPP
#define ENEMY_SHIP_HPP

#include "Ship.hpp"
#include "Player.hpp"
#include <random>

class EnemyShip : public Ship {
public:
    EnemyShip(const sf::Vector2f& position, const std::string& texturePath)
        : Ship(position, texturePath), randomGenerator(std::random_device()()), moveDistribution(-0.2f, 0.2f) {}

    virtual void update(PlayerShip* player) {
        float randomMove = moveDistribution(randomGenerator);
        sprite.move(randomMove, Settings::ENEMY_SPEED);
        if (shooting_clock.getElapsedTime().asSeconds() > Settings::ENEMY_SHOOTING_TIME) {
            shooting_clock.restart();
            if (shouldShoot()){
            shoot();
            }
        }
        updateEnemyAmmos();
    }

    ~EnemyShip() {}

    sf::Vector2f getGunPosition() override {
        sf::Vector2f gun_position = sprite.getPosition();
        gun_position.x += getGlobalBounds().width / 2.0f;
        gun_position.y += getGlobalBounds().height;
        return gun_position;
    }

    bool shouldShoot() const {
        return (static_cast<double>(rand()) / RAND_MAX) < Settings::ENEMY_SHOOT_CHANCE;
    }

    virtual void shoot() {
        enemy_ammos.push_back(std::make_unique<Ammo>(getGunPosition(), "sprites/ammo.png", Settings::ENEMY_AMMO_SPEED));
    }

    void updateEnemyAmmos() {
        for (auto it = enemy_ammos.begin(); it != enemy_ammos.end();) {
            (*it)->update();
            if ((*it)->isOutOfBounds()) {
                it = enemy_ammos.erase(it);
            } else {
                ++it;
            }
        }
    }

    const std::vector<std::unique_ptr<Ammo>>& getAllEnemyAmmos() const {
        return enemy_ammos;
    }

    std::vector<std::unique_ptr<Ammo>>& getEnemyAmmos() {
        return enemy_ammos;
    }

protected:
    sf::Clock shooting_clock;
    std::vector<std::unique_ptr<Ammo>> enemy_ammos;
    std::default_random_engine randomGenerator;
    std::uniform_real_distribution<float> moveDistribution;
};

class GreenEnemy : public EnemyShip {
public:
    GreenEnemy(const sf::Vector2f& position, PlayerShip* player)
        : EnemyShip(position, "sprites/green.png") {}

    ~GreenEnemy() {}

    void update(PlayerShip* player) override {
        EnemyShip::update(player);
        sprite.move(0, 0.1f);
    }

};

class RedEnemy : public EnemyShip {
public:
    RedEnemy(const sf::Vector2f& position, PlayerShip* player)
        : EnemyShip(position, "sprites/red.png") {}

    ~RedEnemy() {}

    void update(PlayerShip* player) override {
        EnemyShip::update(player);
        sf::Vector2f playerPosition = player->getPosition();
        float moveDirection = (playerPosition.x > sprite.getPosition().x) ? 0.35f : -0.35f;
        sprite.move(moveDirection * Settings::ENEMY_SPEED, 0.3f);
    }

    void shoot() override {}

};

class YellowEnemy : public EnemyShip {
public:
    YellowEnemy(const sf::Vector2f& position, PlayerShip* player)
        : EnemyShip(position, "sprites/yellow.png") {}

    ~YellowEnemy() {}

    void update(PlayerShip* player) override {
        EnemyShip::update(player);
    }
};

class PurpleEnemy : public EnemyShip {
public:
    PurpleEnemy(const sf::Vector2f& position, PlayerShip* player) : EnemyShip(position, "sprites/purple_1.png") {}

    ~PurpleEnemy() {}

    void update(PlayerShip* player) override {
        EnemyShip::update(player);
    }

    void shoot() override {
        sf::Vector2f gun_position = getGunPosition();
        gun_position.x -= 5;
        enemy_ammos.push_back(std::make_unique<Ammo>(gun_position, "sprites/ammo.png", Settings::ENEMY_AMMO_SPEED));
        gun_position.x += 10;
        enemy_ammos.push_back(std::make_unique<Ammo>(gun_position, "sprites/ammo.png", Settings::ENEMY_AMMO_SPEED));
    }

};

#endif // ENEMY_SHIP_HPP
