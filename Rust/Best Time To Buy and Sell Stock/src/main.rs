fn main() {
    let prices = vec![1,2];
    println!("{}", max_profit(prices))
}

fn max_profit(prices: Vec<i32>) -> i32 {
    let (mut minima_index, mut maxima_index) = (0, 0);
    let mut most_profit = 0;

    for index in 0..prices.len(){
        if &prices[index] > &prices[maxima_index]{
            maxima_index = index;
        }

        if &prices[index] < &prices[minima_index]{
            maxima_index = index;
            minima_index = index;
        }

        let current_profit = &prices[maxima_index] - &prices[minima_index];

        if current_profit > most_profit {
            most_profit = current_profit
        }
    }

    return most_profit
}