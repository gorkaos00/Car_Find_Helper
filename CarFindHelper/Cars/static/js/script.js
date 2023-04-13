
function next_tab() {
    const button_next = document.querySelector('.next-tab-button');
    const button_prev = document.querySelector('.prev-tab-button');
    if (button_next.innerText === 'Size and Drive') {
        document.getElementById('size-drive-tab').click();

    } else if (button_next.innerText === 'Economic and Power') {
        document.getElementById('eco-power-tab').click();
    }
}

function prev_tab(){
    const button_next = document.querySelector('.next-tab-button');
    const button_prev = document.querySelector('.prev-tab-button');
      if (button_prev.innerText === 'Size and Drive') {
      document.getElementById('size-drive-tab').click();
    } else if (button_prev.innerText === 'Budget and Age') {
          document.getElementById('budget-age-tab').click();
    }

}

function tab_function(tab) {
    const button_next = document.querySelector('.next-tab-button');
    const button_prev = document.querySelector('.prev-tab-button');
    var styling1 ={
        "background":"white",
        "border-top":"none",
    }
    var styling2 ={
        "background":"white",
        "border-top":"solid",
        "border-width":"1px"
    }
    var tab2=document.getElementById('type-drive-tab-box');
    var tab1=document.getElementById('budget-age-tab-box');
    var tab3=document.getElementById('eco-power-tab-box');

    if (tab === 2) {
        button_next.innerHTML = 'Economic and Power';
        button_prev.innerHTML = 'Budget and Age';
        document.getElementById('budget-age').style.display = 'none';
        document.getElementById('type-drive').style.display = 'grid';
        document.getElementById('eco-power').style.display = 'none';
        Object.assign(tab1.style,styling2);
        Object.assign(tab2.style,styling1);
        Object.assign(tab3.style,styling2);

        button_prev.addEventListener('click', button_prev.disabled = false);
        button_next.addEventListener('click', button_next.disabled = false);
    } else if (tab === 1) {
        button_next.innerHTML = 'Size and Drive';
        button_prev.innerHTML = '';
        document.getElementById('budget-age').style.display = 'block';
        document.getElementById('type-drive').style.display = 'none';
        document.getElementById('eco-power').style.display = 'none';
        Object.assign(tab1.style,styling1);
        Object.assign(tab2.style,styling2);
        Object.assign(tab3.style,styling2);
        button_next.addEventListener('click', button_next.disabled = false)
        button_prev.addEventListener('click', button_prev.disabled = true)
    } else if (tab === 3) {
        button_next.innerHTML = '';
        button_prev.innerHTML = 'Size and Drive';
        document.getElementById('budget-age').style.display = 'none';
        document.getElementById('type-drive').style.display = 'none';
        document.getElementById('eco-power').style.display = 'block';
        Object.assign(tab1.style,styling2);
        Object.assign(tab2.style,styling2);
        Object.assign(tab3.style,styling1);
        button_prev.addEventListener('click', button_prev.disabled = false)
        button_next.addEventListener('click', button_next.disabled = true)
    }
}

function find_tab(clicked){
    var radio = document.querySelector('input[type=radio][name=find-tab]:checked');

    if(clicked===1){
        window.location="/find"

    }
    if(clicked===2){
         window.location="/about"

    }
}

