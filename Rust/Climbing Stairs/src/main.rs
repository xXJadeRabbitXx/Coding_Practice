fn main() {
    print!("{}", climb_stairs(10))
}

fn climb_stairs(n: u8) -> u32{
    assert!(n<46);

    let (mut a, mut b) = (1u32, 1u32);

    for _i in 0..n-1 {
        let c = a + b;
        a = b;
        b = c;
    }

    return b;
}