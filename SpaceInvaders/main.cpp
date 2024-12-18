// g++ -c main.cpp -I"C:\\Users\\Prezes\\Documents\\cpp_libs\\SFML\\include"    
// g++ main.o -o main -L"C:\\Users\\Prezes\\Documents\\cpp_libs\\SFML\\lib" -lsfml-graphics -lsfml-window -lsfml-system
// ./main
#include <SFML/Graphics.hpp>
#include <cstdlib>
#include "Settings.hpp"
#include "Ship.hpp"
#include "Player.hpp"
#include "Window.hpp"


int main() {
    Window gameWindow;
    gameWindow.run();

    return 0;
}
