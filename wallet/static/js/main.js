$(document).ready(function(){

    // LOGIN

    $('#result').hide();

    const user = 'usuario@alke.com';
    const pass = '1234';
    
    $('#loginForm').submit(function(e){
        e.preventDefault();

        const emailVal = $('#email').val();
        const passVal = $('#password').val();

        if(emailVal === user && passVal === pass){
            localStorage.setItem('user',emailVal);
            $('#result').html('')

            $('#result').append(`
                <div class="alert alert-success" role="alert">
                Bienvenido ${emailVal}
                </div>
            `)
            .slideDown();

            setTimeout(function () {
                window.location.href = "menu.html";
            }, 3000);
        }else{

            $('#result').html('')
            
            $('#result').append(`
                <div class="alert alert-danger" role="alert">
                Los datos ingresados son incorrectos
                </div>
            `)
            .slideDown();

            setTimeout(function () {
                $('#result').slideUp()
            }, 3000);
        }
    });

    // MENU

    let saldo = Number(localStorage.getItem('saldo')) || 0;
    let userCurrent = localStorage.getItem('user') || '';

    $('#saldo').text(saldo);

    if(userCurrent != ''){
        $('#user-current').text('Hola '+ userCurrent);
    }else{
        $('#user-current').text('Hola usuario.');
    }
    

    $('#deposit').click(function(e){
        e.preventDefault();
        showLegends('depositar','deposit');
    });

    $('#sendMoney').click(function(e){
        e.preventDefault();
        showLegends('transferencia de fondos','sendmoney');
    });

    $('#lastMov').click(function(e){
        e.preventDefault();
        showLegends('últimos movimientos','transactions');
    }); 

    $('#resultsMenu').hide();

    function showLegends(message,link) {
      $('#resultsMenu').append(`
        <div class="alert alert-success alert-dismissible fade show" role="alert">
        <p>redirigiendo a ${message}</p>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
      `)
      .slideDown();

      setTimeout(() => {
        window.location.href = `${link}.html`;
      }, 1500);
    }

    // SEND MONEY

    const contacts = [
        { name: "John", lastname: "Doe", cbu: "123456789", alias:"john.doe", bank: "ABC Bank" },
        { name: "Jane", lastname: "Smith", cbu: "987654321", alias:"jane.smith", bank: "XYZ Bank" }
    ];
    

    $('#filter').on('input', function () {
        const value = $(this).val();
        renderContacts(value);
    });

    function renderContacts(filterText = "") {
        const $list = $('#clientsList');
        const $dataList = $('#contacts-list');
        $list.empty();
        $dataList.empty();

        const text = filterText.toLowerCase();

        const filteredContacts = contacts.filter(valor =>
            valor.name.toLowerCase().includes(text) ||
            valor.lastname.toLowerCase().includes(text) ||
            valor.alias.toLowerCase().includes(text) || 
            valor.name.toLowerCase() +' '+ valor.lastname.toLowerCase()== text
        );

        if (filteredContacts.length === 0) {
            $list.append(`
                <li class="list-group-item text-muted">
                    No se encontraron contactos
                </li>
            `);
            return;
        }

        filteredContacts.forEach((val, i) => {
            const realIndex = contacts.indexOf(val); // índice real

            $list.append(`
                <li class="list-group-item" data-index="${realIndex}">
                    <div class="contact-info">
                        <span class="me-2"><strong>Nombre: </strong>${val.name} ${val.lastname}</span>
                        <span class="me-2"><strong>RUT: </strong> ${val.cbu}</span>
                        <span class="me-2"><strong>Alias: </strong> ${val.alias}</span>
                        <span><strong>Bank: </strong> ${val.bank}</span>
                    </div>
                </li>
            `);

            $dataList.append(`
                <option value="${val.name} ${val.lastname}"></option>
            `)
        });
    }

  

    renderContacts();

    $('#addContact').on('shown.bs.modal', function () {
        $('#name').focus();
    });

    $('#saveClient').click(function(e){
        e.preventDefault();
        let isValid = true;
        let requiredFields = ["#name", "#lastname", "#alias", "#bank", "#cbu"];

        requiredFields.forEach(function (field) {
            if ($(field).val().trim() === "") {
                isValid = false;
                $(field).addClass("is-invalid");
            } else {
                $(field).removeClass("is-invalid");
            }
        });

        let cbu = $('#cbu').val().trim();
        let cbuRegex = /^[0-9]{9}$/;

        if (!cbuRegex.test(cbu)) {
            isValid = false;
            $('#cbu').addClass("is-invalid");
        }

        if (!isValid) {
            
            $('#resultModal').html('');
            $('#resultModal').hide();
            $('#resultModal').append(`
                <div class="alert alert-danger" role="alert">
                    Verifique los campos obligatorios. El CBU debe tener 9 dígitos numéricos.
                </div>
            `)
            .slideDown();
            return;
        }else{
            contacts.push({
                name: $('#name').val(),
                lastname: $('#lastname').val(),
                cbu: cbu,
                alias: $('#alias').val(),
                bank: $('#bank').val()
            }); 

            $('#saveClient').blur();
            bootstrap.Modal.getInstance($('#addContact'))?.hide();
        }
        
    });

    $('#addContact').on('hide.bs.modal',function () {
       renderContacts(); 
    });

    let selectedContact;

    $('#sendMoneyBtn').hide();

    $('#clientsList').on('click', 'li.list-group-item', function (e) {
        e.preventDefault();

        const index = Number($(this).data('index'));
        selectedContact = contacts[index];

        $('#clientsList li.list-group-item').removeClass('active');
        $(this).addClass('active');

        if(selectedContact){
            $('#sendMoneyBtn').slideDown();
        }
    });

    $('#sendMoneyBtn').on('click', sendM);

    function sendM(){
        const amountN = Number($('#amount').val());

        if (!amountN || amountN <= 0) {
            console.log(amountN)
            $('#resultsSend').html('');
            $('#resultsSend').hide();
            $('#resultsSend').append(`
                <div class="alert alert-danger" role="alert">
                    Ingresa un monto válido
                </div>
            `)
            .slideDown();

            setTimeout(function () {
                $('#resultsSend').slideUp()
            }, 3000);
            return;
        }   

        if(!selectedContact){
            $('#resultsSend').html('');
            $('#resultsSend').hide();
            $('#resultsSend').append(`
                <div class="alert alert-danger" role="alert">
                    Selecciona un contacto
                </div>
            `)
            .slideDown();

            setTimeout(function () {
                $('#resultsSend').slideUp()
            }, 3000);
            return;
        }

        let saldoCurrent = Number(localStorage.getItem("saldo")) || 0;

        const newSaldo = saldoCurrent - amountN;

        if(newSaldo < 0){
            $('#resultsSend').html('');
            $('#resultsSend').hide();
            $('#resultsSend').append(`
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <p>Saldo insuficiente</p>
                </div>
            `)
            .slideDown();
            return;
        }

        localStorage.setItem("saldo", String(newSaldo));
        const trans = { type: `Transferencia a ${selectedContact['name']} ${selectedContact['lastname']}`, value: amountN , use: 'transferencia'};

        if(localStorage.getItem('transactions')){
            const localS = JSON.parse(localStorage.getItem('transactions'));
            localS.push(trans);
            localStorage.setItem('transactions', JSON.stringify(localS));
        }else{
            const currentTrans = [];
            currentTrans.push(trans);
            localStorage.setItem('transactions', JSON.stringify(currentTrans));
        }   

        $('#resultsSend').html('');
        $('#resultsSend').hide();
        $('#resultsSend').append(`
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <p>Se ha enviado $${amountN} a ${selectedContact.name} ${selectedContact.lastname}</p>
            </div>
        `)
        .slideDown();

        setTimeout(() => {  
            window.location.href = 'menu.html';
        }, 2000);
    }



    // DEPOSIT

    $('#resultsDeposit').hide();

    const form = document.getElementById('formDeposit');
    const amount = document.getElementById('amount');

    if(form){
        form.addEventListener('submit', (event) => {
                event.preventDefault();

                $('#resultsDeposit').html('');

                const amountN = Number(amount.value);
            
                if (!amountN || amountN <= 0) {
                    $('#resultsDeposit').append(`
                        <div class="alert alert-danger alert-dismissible fade show" role="alert">
                            <p>Ingresa un monto válido</p>
                        </div>
                    `)
                    .slideDown();
                    
                    setTimeout(function () {
                        $('#resultsDeposit').slideUp()
                    }, 3000);
                    return;
                }

                let saldoCurrent = Number(localStorage.getItem("saldo")) || 0;

                const newSaldo = saldoCurrent + amountN;

                localStorage.setItem("saldo", String(newSaldo));

                const trans = { type: 'Deposito', value: amountN };

                if(localStorage.getItem('transactions')){
                    const localS = JSON.parse(localStorage.getItem('transactions'));
                    localS.push(trans);
                    localStorage.setItem('transactions', JSON.stringify(localS));
                }else{
                    const currentTrans = [];
                    currentTrans.push(trans);
                    localStorage.setItem('transactions', JSON.stringify(currentTrans));
                }

                $('#resultsDeposit').append(`
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        <p>Su deposito ha sido de $${amountN}</p>
                    </div>
                `)
                .slideDown();

                setTimeout(() => {  
                    window.location.href = 'menu.html';
                }, 2000);

            })
    }

    

    // TRANSACTIONS

    let transactions = [];

    if (localStorage.getItem('transactions')) {
        transactions = JSON.parse(localStorage.getItem('transactions'));
    }

    function getTipoTransaccion(tipo) {
        return tipo;
    }

    function mostrarUltimosMovimientos(filtro) {
        $('#transact').empty();

        let filtradas = transactions;

        if (filtro !== 'all') {
            filtradas = transactions.filter(t => t.use === filtro);
        }

        if (filtradas.length === 0) {
            $('#transact').append(`
                <li class="list-group-item text-center">
                    No hay movimientos
                </li>
            `);
            return;
        }

        filtradas.forEach(t => {
            let color = '';
            let icon = '';
            if(t.use == 'transferencia'){
                color = 'redC';
                icon = 'fa-solid fa-arrow-down'
            }else{
                color = 'greenC';
                icon = 'fa-solid fa-arrow-up'
            }
            $('#transact').append(`
                <li class="list-group-item">
                    ${getTipoTransaccion(t.type)} - <strong class="${color}">$${t.value} <i class="me-2 ${icon}"></i></strong>
                </li>
            `);
        });
    }

    $('#selectType').on('change', function () {
        let filtro = $(this).val();

        if (filtro === 'Tipo de transacción') {
            mostrarUltimosMovimientos('all');
        } else {
            mostrarUltimosMovimientos(filtro);
        }
    });

    mostrarUltimosMovimientos('all');
    

});