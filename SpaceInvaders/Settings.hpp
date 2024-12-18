// settings.hpp
#pragma once

namespace Settings {
    constexpr int WINDOW_WIDTH = 600;
    constexpr int WINDOW_HEIGHT = 800;

    // Player
    constexpr int SHIP_STARTING_X = WINDOW_WIDTH / 2;
    constexpr int SHIP_STARTING_Y = 9 * WINDOW_HEIGHT / 10;
    constexpr int PLAYER_LIVES_START = 3;
    constexpr double PLAYER_SPEED = 0.25f;
    constexpr double PLAYER_AMMO_SPEED = -0.8f;
    constexpr double PLAYER_SHOOTING_TIME = 0.5f;

    // Enemy
    constexpr int NUM_ENEMY_SHIPS = 10;
    constexpr int ENEMY_RESPAWN_TIME = 4;
    constexpr int ENEMY_SHOOTING_TIME = 1;
    constexpr double ENEMY_SHOOT_CHANCE = 0.4f;
    constexpr double ENEMY_SPEED = 0.25f;
    constexpr double ENEMY_AMMO_SPEED = 0.6f;
}
