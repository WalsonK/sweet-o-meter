use super::mlp_struct::MLP;
use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;

#[no_mangle]
extern "C" fn create_mlp(arr: *const i32, len: i32, nb_seed: u8) -> *mut MLP {
    let mut model = Box::new(MLP {
        layers: 0,
        neurons_per_layer: Vec::new(),
        weights: Vec::new(),
        neuron_data: Vec::new(),
        deltas: Vec::new(),
    });

    // Convert arr to slice
    let arr_slice = unsafe { std::slice::from_raw_parts(arr, len as usize) };

    // Create seed
    let seed: [u8; 32] = [nb_seed; 32];

    // Calc layer & neurons per layer
    model.layers = (len - 1) as usize;
    model.neurons_per_layer = arr_slice.iter().map(|&x| x as usize).collect::<Vec<usize>>();

    // Weights Initialisation
    let mut rng: StdRng = SeedableRng::from_seed(seed);
    for layer in 0..=model.layers {

        for i in 0..=model.neurons_per_layer[layer- 1] {
            model.weights[layer].push(Vec::new());
            for j in 0..=model.neurons_per_layer[layer] {
                let weight = if j == 0 {
                    0.0f32
                } else {
                    rng.gen_range(-1.0f32..=1.0f32)
                };
                model.weights[layer][i].push(weight);
            }
        }
    }

    // neuron_data Initialisation:  0.0 for i=0 else 1.0
    for layer in 0..=model.layers {
        let mut layer_data = Vec::new();
        for i in 0..=model.neurons_per_layer[layer] {
            let value = if i == 0 {
                1.0f32
            } else {
                0.0f32
            };
            layer_data.push(value);
        }
        model.neuron_data.push(layer_data);
    }

    // Deltas Initialisation : 0.0
    for layer in 0..=model.layers {
        let mut layer_deltas = Vec::new();
        for _ in 0..=model.neurons_per_layer[layer]{
            let delta= 0.0f32;
            layer_deltas.push(delta);
        }
        model.deltas.push(layer_deltas);
    }

    print_created_model(&model);

    let leaked = Box::leak(model);
    leaked
}

fn print_created_model(model : &MLP) {
    // Layers & neurons per layer
    println!("PMC : layers : {}", model.layers);
    println!("PMC : n per layer len : {}", model.neurons_per_layer.len());
    for i in 0..model.neurons_per_layer.len() {
        println!("PMC : layer[{}] : {}", i, model.neurons_per_layer[i]);
    }

    // Weights
    println!("PMC: Weights len : {}", model.weights.len());
    for layer in 0..=model.layers {
        for i in 0..model.weights[layer].len() {
            for j in 0..model.weights[layer][i].len() {
                println!("-- weights[{}][{}][{}]: {}", layer, i, j,  model.weights[layer][i][j]);
            }
        }
    }

    // Neurons res
    println!("PMC: Neuron data len : {}", model.neuron_data.len());
    for i in 0..model.neuron_data.len(){
        for j in 0..model.neuron_data[i].len(){
            println!("-- neuronData[{}][{}]: {}", i, j, model.neuron_data[i][j]);
        }
    }

    // Deltas
    println!("PMC: deltas len : {}", model.deltas.len());
    for i in 0..model.deltas.len(){
        for j in 0..model.deltas[i].len(){
            println!("- deltas[{}][{}]: {}", i, j, model.deltas[i][j]);
        }
    }
}