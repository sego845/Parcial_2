from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
import json
import os

app = FastAPI(title="Sego - Panadería API")


class Cliente(BaseModel):
    id: int
    nombre: str
    email: EmailStr


class Pan(BaseModel):
    id: int
    tipo: str
    precio: float
    peso: float


class Pedido(BaseModel):
    id: int
    cliente_id: int
    panes: List[int]


class BaseRepositorio:
    def __init__(self, archivo: str):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            self._guardar([])

    def _cargar(self):
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar(self, datos):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)


class RepositorioCliente(BaseRepositorio):
    def listar(self):
        return self._cargar()

    def obtener(self, cliente_id: int):
        for cliente in self._cargar():
            if cliente["id"] == cliente_id:
                return cliente
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    def crear(self, cliente: Cliente):
        datos = self._cargar()
        if any(c["id"] == cliente.id for c in datos):
            raise HTTPException(status_code=400, detail="El ID ya existe")
        datos.append(cliente.dict())
        self._guardar(datos)
        return cliente

    def actualizar(self, cliente_id: int, cliente: Cliente):
        datos = self._cargar()
        for i, c in enumerate(datos):
            if c["id"] == cliente_id:
                datos[i] = cliente.dict()
                self._guardar(datos)
                return cliente
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    def eliminar(self, cliente_id: int):
        datos = self._cargar()
        nuevos = [c for c in datos if c["id"] != cliente_id]
        self._guardar(nuevos)
        return {"message": "Cliente eliminado"}


class RepositorioPan(BaseRepositorio):
    def listar(self):
        return self._cargar()

    def obtener(self, pan_id: int):
        for pan in self._cargar():
            if pan["id"] == pan_id:
                return pan
        raise HTTPException(status_code=404, detail="Pan no encontrado")

    def crear(self, pan: Pan):
        datos = self._cargar()
        if any(p["id"] == pan.id for p in datos):
            raise HTTPException(status_code=400, detail="El ID ya existe")
        datos.append(pan.dict())
        self._guardar(datos)
        return pan

    def actualizar(self, pan_id: int, pan: Pan):
        datos = self._cargar()
        for i, p in enumerate(datos):
            if p["id"] == pan_id:
                datos[i] = pan.dict()
                self._guardar(datos)
                return pan
        raise HTTPException(status_code=404, detail="Pan no encontrado")

    def eliminar(self, pan_id: int):
        datos = self._cargar()
        nuevos = [p for p in datos if p["id"] != pan_id]
        self._guardar(nuevos)
        return {"message": "Pan eliminado"}


class RepositorioPedido(BaseRepositorio):
    def listar(self):
        return self._cargar()

    def obtener(self, pedido_id: int):
        for pedido in self._cargar():
            if pedido["id"] == pedido_id:
                return pedido
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    def crear(self, pedido: Pedido):
        datos = self._cargar()
        if any(p["id"] == pedido.id for p in datos):
            raise HTTPException(status_code=400, detail="El ID ya existe")
        datos.append(pedido.dict())
        self._guardar(datos)
        return pedido

    def actualizar(self, pedido_id: int, pedido: Pedido):
        datos = self._cargar()
        for i, p in enumerate(datos):
            if p["id"] == pedido_id:
                datos[i] = pedido.dict()
                self._guardar(datos)
                return pedido
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    def eliminar(self, pedido_id: int):
        datos = self._cargar()
        nuevos = [p for p in datos if p["id"] != pedido_id]
        self._guardar(nuevos)
        return {"message": "Pedido eliminado"}


clientes_repo = RepositorioCliente("clientes.json")
panes_repo = RepositorioPan("panes.json")
pedidos_repo = RepositorioPedido("pedidos.json")


@app.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    return clientes_repo.listar()

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    return clientes_repo.obtener(cliente_id)

@app.post("/clientes", response_model=Cliente)
def crear_cliente(cliente: Cliente):
    return clientes_repo.crear(cliente)

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, cliente: Cliente):
    return clientes_repo.actualizar(cliente_id, cliente)

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    return clientes_repo.eliminar(cliente_id)


@app.get("/panes", response_model=List[Pan])
def listar_panes():
    return panes_repo.listar()

@app.get("/panes/{pan_id}", response_model=Pan)
def obtener_pan(pan_id: int):
    return panes_repo.obtener(pan_id)

@app.post("/panes", response_model=Pan)
def crear_pan(pan: Pan):
    return panes_repo.crear(pan)

@app.put("/panes/{pan_id}", response_model=Pan)
def actualizar_pan(pan_id: int, pan: Pan):
    return panes_repo.actualizar(pan_id, pan)

@app.delete("/panes/{pan_id}")
def eliminar_pan(pan_id: int):
    return panes_repo.eliminar(pan_id)


@app.get("/pedidos", response_model=List[Pedido])
def listar_pedidos():
    return pedidos_repo.listar()

@app.get("/pedidos/{pedido_id}", response_model=Pedido)
def obtener_pedido(pedido_id: int):
    return pedidos_repo.obtener(pedido_id)

@app.post("/pedidos", response_model=Pedido)
def crear_pedido(pedido: Pedido):
    return pedidos_repo.crear(pedido)

@app.put("/pedidos/{pedido_id}", response_model=Pedido)
def actualizar_pedido(pedido_id: int, pedido: Pedido):
    return pedidos_repo.actualizar(pedido_id, pedido)

@app.delete("/pedidos/{pedido_id}")
def eliminar_pedido(pedido_id: int):
    return pedidos_repo.eliminar(pedido_id)
