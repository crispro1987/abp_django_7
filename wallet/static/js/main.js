$(document).ready(function(){

    const select = document.getElementById('cuentaSelect');
    const saldo = document.getElementById('saldo');

    select.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const balance = selectedOption.getAttribute('data-balance');

        saldo.textContent = `$${balance}`;
    });
    

});