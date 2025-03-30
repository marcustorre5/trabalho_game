# Space Shooter Demo

## Descrição
Space Shooter Demo é um jogo de nave do tipo *Shoot 'Em Up* (SHMUP) desenvolvido em Python utilizando a biblioteca **Pygame**. O jogo oferece uma experiência de ação intensa, onde você controla uma nave espacial que precisa destruir ondas de inimigos enquanto coleta power-ups e desvia de tiros. À medida que avança, a dificuldade aumenta com novos tipos de inimigos e chefes desafiadores. O objetivo final é alcançar a maior pontuação possível e sobreviver o máximo que puder.

## Funcionalidades
- **Movimento da nave**: Use as teclas de direção ou as setas do teclado para mover a nave.
- **Tiros**: Pressione a barra de espaço para atirar lasers contra os inimigos.
- **Power-ups**: Coleta power-ups para obter bônus temporários, como tiros triplos e escudo de proteção.
- **Inimigos e Chefes**: Enfrente diversos inimigos com padrões de ataque variados, incluindo inimigos que atiram e inimigos em movimento zigue-zague. Enfrente um chefe desafiador ao alcançar a pontuação de 1000 pontos.
- **Mudança de nível**: O jogo evolui para níveis mais difíceis com novos inimigos à medida que você acumula pontos.
- **Pontuação**: Acompanhe sua pontuação e o *high score*.

## Instruções
1. **Movimento**: Use as setas <- e -> para mover a nave.
2. **Atirar**: Pressione a tecla **ESPAÇO** para disparar lasers.
3. **Power-ups**: Coloque a nave sobre os power-ups para coletá-los.
4. **Pausar o jogo**: Pressione a tecla **P**.
5. **Reiniciar o jogo**: Após a tela de game over, pressione **R** para reiniciar ou **Q** para sair.

## Como Jogar
1. Clone ou baixe o repositório.
2. Instale a biblioteca **Pygame**:
   ```bash
   pip install pygame
   ```
3. Execute o script **space_shooter.py**:
   ```bash
   python space_shooter.py
   ```
4. Aproveite o jogo e tente alcançar a maior pontuação possível!

## Recursos do Jogo
- **Gráficos**: Gráficos 2D em estilo retro com várias imagens de fundo e sprites para a nave, inimigos e power-ups.
- **Áudio**: Efeitos sonoros para tiros, explosões e coleta de power-ups.
- **Progressão**: O jogo se torna mais difícil conforme o jogador avança, com novos inimigos, maior velocidade e chefes especiais.

## Tela de Pausa
- Durante o jogo, pressione **P** para pausar. Você poderá retomar o jogo pressionando **P** novamente.

## Tela de Game Over
- Quando o jogador perder todas as vidas, a tela de *Game Over* aparecerá. O jogador poderá reiniciar o jogo pressionando **R** ou sair pressionando **Q**.

## Personalização
Você pode adicionar mais inimigos, naves ou power-ups editando as classes no código. Para criar novas fases, adicione mais imagens de fundo e crie novos tipos de inimigos.

## Contribuições
Se você encontrar algum erro ou desejar adicionar novas funcionalidades, sinta-se à vontade para contribuir com *pull requests* ou abrir *issues*.

## Licença
Este projeto é licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Imagens e Sons
Certifique-se de ter os seguintes arquivos na pasta **assets** para garantir que o jogo funcione corretamente:
- player.png
- enemy1.png
- enemy2.png
- enemy3.png
- boss.png
- bullet.png
- powerup.png
- background1.png
- background2.png
- background3.png
- shoot.wav
- explosion.wav
- powerup.wav

## Agradecimentos
- Desenvolvido por **Marcus Torres** usando **Pygame**.
