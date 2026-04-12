# 📌 SecGar — Contexto General del Proyecto (Versión Extendida)

---

# 1. 🧭 Definición del Sistema

## 1.1 Naturaleza del proyecto

SecGar es una plataforma digital tipo **marketplace bilateral** que conecta:

- Oferta: propietarios de espacios de estacionamiento
- Demanda: usuarios que necesitan estacionar su vehículo

La plataforma no es propietaria de los activos, sino que actúa como:

> Intermediario tecnológico + facilitador de confianza + regulador indirecto del mercado

---

## 1.2 Tipo de sistema

- Plataforma web (inicialmente)
- Escalable a aplicación móvil
- Arquitectura orientada a servicios (a futuro)
- Basado en interacción usuario ↔ sistema ↔ usuario

---

## 1.3 Dominio del problema

El sistema pertenece al dominio de:

- Movilidad urbana
- Optimización de recursos subutilizados
- Economía colaborativa (sharing economy)

---

# 2. 🎯 Problema y Justificación

## 2.1 Problema central

En entornos urbanos existe una desconexión entre:

- Espacios disponibles (infrautilizados)
- Demanda activa de estacionamiento

Esto genera:

- Pérdida de tiempo en búsqueda
- Ineficiencia en uso de infraestructura
- Riesgos en acuerdos informales

---

## 2.2 Problemas secundarios

- Falta de confianza entre desconocidos
- Ausencia de estandarización en precios
- Fricción en el proceso de arriendo
- Baja visibilidad de oferta disponible

---

## 2.3 Propuesta de valor

SecGar propone:

- Centralización de oferta y demanda
- Interfaz simple de uso
- Sistema de reservas estructurado
- Mecanismos de confianza (a definir)
- Orientación de precios basada en datos

---

# 3. 👥 Actores del Sistema

## 3.1 Propietario (Proveedor)

Características:

- Posee un espacio físico disponible
- Busca monetizar un activo subutilizado

Capacidades:

- Publicar espacio
- Definir condiciones
- Establecer precio
- Aceptar o automatizar reservas

---

## 3.2 Arrendatario (Consumidor)

Características:

- Necesita estacionamiento temporal o recurrente

Capacidades:

- Buscar espacios
- Filtrar opciones
- Reservar
- Pagar

---

## 3.3 Plataforma (SecGar)

Responsabilidades:

- Orquestar la interacción
- Reducir fricción
- Generar confianza
- Optimizar matching entre oferta y demanda

---

# 4. 📦 Alcance del Sistema

## 4.1 Incluye

- Estacionamientos para vehículos automotrices
- Arriendos por:
  - Hora
  - Día
  - Mes
- Espacios:
  - Privados
  - Residenciales
  - Comerciales

---

## 4.2 Excluye

- Bicicletas
- Motos industriales
- Bodegaje
- Usos no relacionados a estacionamiento vehicular

---

## 4.3 Restricciones

- No intervención física en los espacios
- Dependencia de veracidad del propietario
- Dependencia de comportamiento del usuario

---

# 5. 💰 Modelo de Negocio

## 5.1 Estructura

Modelo tipo marketplace:

- C2C (consumer to consumer)

---

## 5.2 Fuente de ingresos

Principal:

- Comisión por transacción

Posibles futuras:

- Promoción de espacios (boost)
- Suscripción premium propietarios
- Servicios adicionales

---

## 5.3 Consideraciones económicas

- Sensibilidad al precio del usuario final
- Incentivo de adopción inicial (baja comisión)
- Necesidad de liquidez del mercado

---

# 6. 📊 Sistema de Pricing

## 6.1 Modelo adoptado

Modelo híbrido:

- Precio definido por el propietario
- Plataforma orienta mediante datos

---

## 6.2 Variables de pricing

- Ubicación (comuna)
- Tamaño del espacio
- Tipo de espacio:
  - Techado
  - Cerrado
  - Subterráneo
- Seguridad
- Demanda estimada

---

## 6.3 Mecanismo de regulación indirecta

La plataforma influye mediante:

- Rango recomendado
- Precio promedio de la zona
- Indicador de competitividad
- Orden en resultados de búsqueda

---

## 6.4 Objetivo del sistema de pricing

- Maximizar ocupación
- Mantener coherencia de mercado
- Evitar precios extremos

---

# 7. ⚙️ Lógica del Sistema

## 7.1 Flujo general

1. Propietario publica espacio
2. Sistema calcula contexto (precio, zona, etc.)
3. Usuario busca espacio
4. Sistema filtra y ordena resultados
5. Usuario reserva
6. Sistema gestiona transacción

---

## 7.2 Matching

El sistema debe optimizar:

- Cercanía
- Precio
- Calidad del espacio
- Probabilidad de conversión

---

## 7.3 Ordenamiento de resultados

Factores posibles:

- Precio competitivo
- Ubicación
- Calidad percibida
- Disponibilidad

---

# 8. 🧠 Principios de Diseño

## 8.1 Simplicidad

Reducir fricción al mínimo.

---

## 8.2 Transparencia

Información clara y visible.

---

## 8.3 Confianza

Reducir incertidumbre entre usuarios.

---

## 8.4 Escalabilidad

Sistema preparado para crecimiento.

---

## 8.5 Neutralidad controlada

La plataforma no impone, pero influye.

---

# 9. 🤖 Enfoque de Desarrollo con IA

## 9.1 Rol de la IA

- Asistente de desarrollo
- Soporte en decisiones
- Generación de código
- Optimización de procesos

---

## 9.2 Reglas para IA

- Usar este documento como contexto base
- No proponer soluciones fuera del alcance
- Priorizar simplicidad sobre complejidad innecesaria
- Alinear decisiones con el modelo de negocio

---

## 9.3 Riesgos a evitar

- Sobreingeniería
- Desalineación con objetivos
- Complejidad innecesaria

---

# 10. 🚀 Estado del Proyecto

Fase actual:

- Definición conceptual
- Diseño del modelo
- Estructuración inicial

---

# 11. 🔮 Evolución Esperada

- Introducción de pricing dinámico
- Mejora de algoritmos de matching
- Sistemas de reputación
- Expansión geográfica

---

# 12. 📌 Fuente de Verdad

Este documento:

- Define el sistema
- Establece límites
- Alinea decisiones

Debe ser actualizado continuamente.

---