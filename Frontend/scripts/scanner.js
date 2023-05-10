async function change_use_scanner(id) {
        const btn = document.getElementById(`btn_use_${id}`);
        let using = btn.getAttribute('data-using').toLowerCase() == 'true' ? true : false;

        let url = `api/scanners/in_use/${id}`;
        let text = 'Не использовать';
        if (using == true) {
            url = `api/scanners/not_in_use/${id}`;
            text = 'Использовать';
        }

        await fetch(url=url)
            .then((resp) => resp.json())
            .then((data) => {
                if (data.status == 0) {
                    btn.textContent = text;
                    btn.setAttribute('data-using', !using);
                }
            })
            .catch(function(error) {
                console.log(error);
            })
}

async function delete_scanner(id) {
    let url = `api/scanners/${id}`;

    await fetch(url, {method: 'DELETE'})
        .then((resp) => resp.json())
        .then(async (data) => {
            if (data.status == 0) {
                await update_scanners_list();
            }
        })
        .catch(function(error) {
            console.log(error);
        })
}


async function update_scanners() {
    let url = `api/scanners/all`;

    await fetch(url=url)
        .then((resp) => resp.json())
        .then((data) => {
            clearContent('scanner-items');
            data.forEach(async (scanner) => {
                addScanner(scanner.id, scanner.name, scanner.active, scanner.in_use);
            })
        })
        .catch(function(error) {
            console.log(error);
        })
}

async function update_scanners_list() {
    let url = `api/scanners/update_all`;
    let btn = document.getElementById('button-update');
    btn.textContent = '------';
//    btn.disabled = true;

    await fetch(url=url)
        .then((resp) => resp.json())
        .then((data) => {
            btn.textContent = 'Обновить список';
//            btn.disabled = false;
            clearContent('scanner-items');
            data.forEach(async (scanner) => {
                addScanner(scanner.id, scanner.name, scanner.active, scanner.in_use);
            })
        })
        .catch(function(error) {
            console.log(error);
        })
}

function addScanner(id, name, active, in_use) {
    const div = document.createElement('div');
    div.className = 'scanner__item';

    const part_1 = `<div class="scanner__info">
                <div>${ id }</div>
                <div>${ name }</div>
                ${ active == true ? `<div class="scanner-active"></div>` : `<div></div>` }
            </div>`

    const part_2 = `<div></div>`;
    const part_3 = `<div class="scanner__actions">
        ${ active == true 
            ? `<button id="btn_use_${ id }" type="submit" class="scanner__button" 
                    data-using="${ in_use }" onclick="change_use_scanner(${ id });">
                ${ in_use == true ? `Не использовать` : `Использовать` }
                </button>` 
            : `<button disabled type="submit" class="scanner__button">Сканнер неактивен</button>`}
        <button id="btn_del_${ id }" type="submit" class="scanner__button button-delete button-red"
            onclick="delete_scanner(${ id });">Удалить</button>
    </div>`;
    div.innerHTML = part_1 + part_2 + part_3;
        
    document.getElementById('scanner-items').appendChild(div);
}

function clearContent(elementID) {
    document.getElementById(elementID).innerHTML = '';
}

async function discovery_scanners() {  
    const subnet = document.getElementById('subnet').value;
    const port = document.getElementById('port').value;
    let btn = document.getElementById('button_hd');
    btn.textContent = '------';
//    btn.disabled = true;

    let url = `api/scanners/search`;

    await fetch(url=url, {
        method: 'POST', 
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            subnet: subnet,
            port: port
            })
        })
        .then((resp) => resp.json())
        .then(async (data) => {
            if (data.status == 0) {
                btn.textContent = 'Искать службы сканирования';
//                btn.disabled = false;
                await update_scanners();
            }
        })
        .catch(function(error) {
            console.log(error);
        })
}
