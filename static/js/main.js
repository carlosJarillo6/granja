const btnBorrar = document.querySelectorAll('.btn-delete')

if(btnBorrar){
    const btnArray = Array.from(btnBorrar);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('borrar')){
                e.preventDefault();
            }
        });
    });

}