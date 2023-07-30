use super::mlp_struct::MLP;

#[no_mangle]
extern "C" fn delete_mlp(model: &mut MLP) {
    unsafe {
        let _ = Box::from_raw(model);
    }
    println!("Model deleted")
}