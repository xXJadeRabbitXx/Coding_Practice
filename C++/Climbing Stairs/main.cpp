#include <iostream>
#include <assert.h>

int climbStairs(int n) {
    assert(n < 46);

    int a = 1, b = 1;

    for (int counter = 0; counter < n-1; counter++)
    {
        int c = a + b;
        a = b;
        b = c;
    }

    return b;
    
}

int main(){
    std::cout << climbStairs(15) << std::endl;
}