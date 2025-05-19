from pydantic import BaseModel, field_validator
from typing import Optional, Literal


class HeadphonesPydantic(BaseModel):
    brand: str
    wireless: bool
    impedance: int
    color: str
    form_factor: Literal['вкладыши', 'накладные', 'вставные', 'полноразмерные']
    noise_cancelling: Optional[bool] = None
    weight: Optional[float] = None

    @field_validator('impedance', 'weight')
    def must_be_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Не, надо положительное")
        return value

    def is_portable(self) -> bool:
        return self.wireless and (self.weight is not None and self.weight <= 300)
