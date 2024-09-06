import pygame
import random
import math

# Inicialización de Pygame
pygame.init()

# Constantes
GRID_SIZE = 50
CELL_SIZE = 10
QUARANTINE_DURATION = 60  # 60 segundos
FPS = 10
DISTANCIA_MINIMA = 10  # Ajusta la distancia mínima para la infección
PROBABILIDAD_INFECCION = 0.5  # Ajusta la probabilidad de infección
FONT_SIZE = 20
TIEMPO_CUBREBOCAS = 60  # 1 minuto en segundos

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
NARANJA = (255, 165, 0)

# Clase Persona
class Persona:
    def __init__(self, x, y, estado="sano"):
        self.x = x
        self.y = y
        self.estado = estado
        self.tiempo_cuarentena = 0
        self.tiempo_cubrebocas = 0  # Tiempo restante del cubrebocas

    def mover(self):
        if self.estado != "cuarentena":
            self.x = max(0, min(GRID_SIZE - 1, self.x + random.choice([-1, 1])))
            self.y = max(0, min(GRID_SIZE - 1, self.y + random.choice([-1, 1])))

    def infectar(self, otra_persona):
        distancia = calcular_distancia(self, otra_persona)
        if distancia <= DISTANCIA_MINIMA and otra_persona.estado == "sano":
            if random.random() < PROBABILIDAD_INFECCION:
                otra_persona.estado = "infectado"

    def poner_cubrebocas(self):
        if self.estado == "sano" and self.tiempo_cubrebocas <= 0:
            self.estado = "protegido"
            self.tiempo_cubrebocas = TIEMPO_CUBREBOCAS

    def poner_en_cuarentena(self):
        if self.estado == "infectado":
            self.estado = "cuarentena"
            self.tiempo_cuarentena = QUARANTINE_DURATION

    def actualizar_tiempo_cubrebocas(self, delta_tiempo):
        if self.estado == "protegido":
            self.tiempo_cubrebocas -= delta_tiempo
            if self.tiempo_cubrebocas <= 0:
                self.estado = "sano"

def calcular_distancia(persona1, persona2):
    dx = persona1.x - persona2.x
    dy = persona1.y - persona2.y
    return math.sqrt(dx*dx + dy*dy)

def update_simulation(personas, delta_tiempo):
    for persona in personas:
        if persona.estado == "infectado":
            for otra_persona in personas:
                persona.infectar(otra_persona)
        if persona.estado == "cuarentena":
            persona.tiempo_cuarentena -= delta_tiempo
            if persona.tiempo_cuarentena <= 0:
                persona.estado = "sano"
        persona.actualizar_tiempo_cubrebocas(delta_tiempo)

def draw_personas(screen, personas, tiempo_simulacion):
    screen.fill(NEGRO)
    for persona in personas:
        color = (
            VERDE if persona.estado == "sano" else
            ROJO if persona.estado == "infectado" else
            AZUL if persona.estado == "protegido" else
            NARANJA
        )
        pygame.draw.rect(screen, color, (persona.x * CELL_SIZE, persona.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Mostrar tiempo de simulación
    font = pygame.font.SysFont(None, FONT_SIZE)
    texto_tiempo = font.render(f"Tiempo de simulación: {int(tiempo_simulacion)}s", True, BLANCO)
    screen.blit(texto_tiempo, (10, 10))

    # Mostrar tiempo de cuarentena para cada persona en cuarentena
    for persona in personas:
        if persona.estado == "cuarentena":
            tiempo_restante = persona.tiempo_cuarentena
            texto_cuarentena = font.render(f"{int(tiempo_restante)}s", True, BLANCO)
            screen.blit(texto_cuarentena, (persona.x * CELL_SIZE, persona.y * CELL_SIZE + CELL_SIZE))
        
        # Mostrar tiempo restante del cubrebocas para cada persona protegida
        if persona.estado == "protegido":
            tiempo_restante_cubrebocas = persona.tiempo_cubrebocas
            texto_cubrebocas = font.render(f"{int(tiempo_restante_cubrebocas)}s", True, BLANCO)
            screen.blit(texto_cubrebocas, (persona.x * CELL_SIZE, persona.y * CELL_SIZE + 2 * CELL_SIZE))

    pygame.display.flip()

def reiniciar_infeccion(personas):
    # Selecciona una persona al azar para infectar
    personas[random.randint(0, len(personas) - 1)].estado = "infectado"

def main():
    # Configuración de la ventana
    width = GRID_SIZE * CELL_SIZE
    height = GRID_SIZE * CELL_SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Simulador de Pandemia")
    
    clock = pygame.time.Clock()
    
    # Crear personas
    personas = [Persona(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(20)]
    personas[0].estado = "infectado"  # Inicialmente un solo infectado
    
    simulation_running = False
    tiempo_simulacion = 0

    # Bucle principal
    while True:
        delta_tiempo = clock.tick(FPS) / 1000  # Tiempo transcurrido en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_running = True
                elif event.key == pygame.K_c:
                    for persona in personas:
                        persona.poner_cubrebocas()
                elif event.key == pygame.K_x:
                    for persona in personas:
                        persona.poner_en_cuarentena()
                elif event.key == pygame.K_a:
                    reiniciar_infeccion(personas)
        
        if simulation_running:
            tiempo_simulacion += delta_tiempo
            for persona in personas:
                persona.mover()
            update_simulation(personas, delta_tiempo)

            # Comprobar si todos están sanos
            todos_sanos = all(persona.estado == "sano" for persona in personas)
            if todos_sanos:
                tiempo_simulacion = 0  # Reinicia el temporizador si todos están sanos

        draw_personas(screen, personas, tiempo_simulacion)

if __name__ == "__main__":
    main()
