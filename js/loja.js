document.addEventListener('DOMContentLoaded', (event) => {
    const rangeInput = document.getElementById('preco');
    const output = document.getElementById('preco-output');
    
    // Atualiza o valor do output inicialmente
    output.value = `R$ ${rangeInput.value}`;
    
    // Adiciona um evento para atualizar o valor do output conforme a barra é movida
    rangeInput.addEventListener('input', function() {
      output.value = `R$ ${this.value}`;
    });
  });