// Arrays para armazenar dados
        let atletas = [];
        let categorias = [];

        // Função para mostrar/ocultar senha
        document.getElementById('mostrar-senha').addEventListener('change', function() {
            const senhaInput = document.getElementById('novo-user-senha');
            senhaInput.type = this.checked ? 'text' : 'password';
        });

        // Função para preview da foto
        document.getElementById('input-foto').addEventListener('change', function(event) {
            const file = event.target.files[0];
            const preview = document.getElementById('foto-preview');
            
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.style.backgroundImage = `url(${e.target.result})`;
                    preview.style.backgroundSize = 'cover';
                    preview.style.backgroundPosition = 'center';
                    preview.innerHTML = '';
                };
                reader.readAsDataURL(file);
            }
        });

        // Função para adicionar categoria
        document.getElementById('add-categoria-btn').addEventListener('click', function() {
            const nomeCategoria = document.getElementById('nova-categoria').value.trim();
            if (nomeCategoria) {
                const categoria = {
                    id: Date.now(),
                    nome: nomeCategoria
                };
                categorias.push(categoria);
                atualizarSelectCategorias();
                document.getElementById('nova-categoria').value = '';
                
                // Feedback visual
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i>';
                this.classList.add('success-feedback');
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('success-feedback');
                }, 1500);
            } else {
                alert('Por favor, digite o nome da categoria.');
            }
        });

        // Função para atualizar selects de categoria
        function atualizarSelectCategorias() {
            const selects = [
                document.getElementById('categoria-atleta'),
                document.getElementById('categoria-operador'),
                document.getElementById('select-categoria-excluir')
            ];

            selects.forEach(select => {
                const firstOption = select.options[0];
                select.innerHTML = '';
                select.appendChild(firstOption);

                categorias.forEach(categoria => {
                    const option = document.createElement('option');
                    option.value = categoria.id;
                    option.textContent = categoria.nome;
                    select.appendChild(option);
                });
            });
        }

        // Função para adicionar atleta
        document.getElementById('add-atleta-btn').addEventListener('click', function() {
            const nomeAtleta = document.getElementById('nome-atleta').value.trim();
            const categoriaId = document.getElementById('categoria-atleta').value;
            const fotoPreview = document.getElementById('foto-preview');
            const fotoSrc = fotoPreview.style.backgroundImage ? fotoPreview.style.backgroundImage.slice(5, -2) : null;

            if (nomeAtleta && categoriaId) {
                const categoria = categorias.find(c => c.id == categoriaId);
                const atleta = {
                    id: Date.now(),
                    nome: nomeAtleta,
                    categoria: categoria.nome,
                    categoriaId: categoriaId,
                    foto: fotoSrc
                };
                atletas.push(atleta);
                atualizarSelectAtletas();
                
                // Limpar campos
                document.getElementById('nome-atleta').value = '';
                document.getElementById('categoria-atleta').value = '';
                fotoPreview.style.backgroundImage = '';
                fotoPreview.innerHTML = '<i class="fas fa-camera"></i>';
                
                // Feedback visual
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Adicionado!';
                this.classList.add('success-feedback');
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('success-feedback');
                }, 2000);
            } else {
                alert('Por favor, preencha todos os campos.');
            }
        });

        // Função para atualizar selects de atletas
        function atualizarSelectAtletas() {
            const selects = [
                document.getElementById('atleta-operador'),
                document.getElementById('select-atleta-excluir')
            ];

            selects.forEach(select => {
                const firstOption = select.options[0];
                select.innerHTML = '';
                select.appendChild(firstOption);

                atletas.forEach(atleta => {
                    const option = document.createElement('option');
                    option.value = atleta.id;
                    option.textContent = atleta.nome;
                    select.appendChild(option);
                });
            });
        }

        // Função para atualizar foto do atleta selecionado
        document.getElementById('atleta-operador').addEventListener('change', function() {
            const atletaId = this.value;
            const atleta = atletas.find(a => a.id == atletaId);
            const fotoAtleta = document.getElementById('foto-atleta');
            
            if (atleta && atleta.foto) {
                fotoAtleta.style.backgroundImage = `url(${atleta.foto})`;
                fotoAtleta.style.backgroundSize = 'cover';
                fotoAtleta.style.backgroundPosition = 'center';
                fotoAtleta.innerHTML = '';
            } else {
                fotoAtleta.style.backgroundImage = '';
                fotoAtleta.innerHTML = '<i class="fas fa-user"></i>';
            }
        });

        // Função para cadastrar usuário
        document.getElementById('cadastrar-usuario-btn').addEventListener('click', function() {
            const nome = document.getElementById('novo-user-nome').value.trim();
            const senha = document.getElementById('novo-user-senha').value.trim();
            
            if (nome && senha) {
                // Feedback visual
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Cadastrado!';
                this.classList.add('success-feedback');
                
                document.getElementById('novo-user-nome').value = '';
                document.getElementById('novo-user-senha').value = '';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('success-feedback');
                }, 2000);
            } else {
                alert('Por favor, preencha todos os campos.');
            }
        });

        // Função para enviar para operador
        document.getElementById('enviar-operador-btn').addEventListener('click', function() {
            const atletaId = document.getElementById('atleta-operador').value;
            const categoriaId = document.getElementById('categoria-operador').value;
            
            if (atletaId && categoriaId) {
                // Feedback visual
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> ENVIADO!';
                this.classList.add('success-feedback');
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('success-feedback');
                }, 2000);
            } else {
                alert('Por favor, selecione um atleta e uma categoria.');
            }
        });

        // Função para excluir atleta
        document.getElementById('excluir-atleta-btn').addEventListener('click', function() {
            const atletaId = document.getElementById('select-atleta-excluir').value;
            
            if (atletaId) {
                if (confirm('Tem certeza que deseja excluir este atleta?')) {
                    atletas = atletas.filter(a => a.id != atletaId);
                    atualizarSelectAtletas();
                    document.getElementById('select-atleta-excluir').value = '';
                    
                    // Reset foto do operador se o atleta excluído estava selecionado
                    const atletaOperador = document.getElementById('atleta-operador');
                    if (atletaOperador.value == atletaId) {
                        atletaOperador.value = '';
                        document.getElementById('foto-atleta').style.backgroundImage = '';
                        document.getElementById('foto-atleta').innerHTML = '<i class="fas fa-user"></i>';
                    }
                    
                    // Feedback visual
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i> Excluído!';
                    this.classList.add('success-feedback');
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('success-feedback');
                    }, 2000);
                }
            } else {
                alert('Por favor, selecione um atleta para excluir.');
            }
        });

        // Função para excluir categoria
        document.getElementById('excluir-categoria-btn').addEventListener('click', function() {
            const categoriaId = document.getElementById('select-categoria-excluir').value;
            
            if (categoriaId) {
                if (confirm('Tem certeza que deseja excluir esta categoria?')) {
                    categorias = categorias.filter(c => c.id != categoriaId);
                    atualizarSelectCategorias();
                    document.getElementById('select-categoria-excluir').value = '';
                    
                    // Feedback visual
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i> Excluída!';
                    this.classList.add('success-feedback');
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('success-feedback');
                    }, 2000);
                }
            } else {
                alert('Por favor, selecione uma categoria para excluir.');
            }
        });

        // Animação de entrada dos cards
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.card');
            cards.forEach((card, index) => {
                card.style.animationDelay = `${index * 0.1}s`;
            });
        });