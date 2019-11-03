from dataclasses import dataclass
from typing import List

from funowl.annotations import Annotation
from funowl.axioms import Axiom
from funowl.base.list_support import empty_list
from funowl.class_expressions import ClassExpression
from funowl.dataproperty_expressions import DataPropertyExpression
from funowl.dataranges import DataRange
from funowl.writers.FunctionalWriter import FunctionalWriter
from funowl.literals import Datatype

"""
DataPropertyAxiom :=
    SubDataPropertyOf | EquivalentDataProperties | DisjointDataProperties |
    DataPropertyDomain | DataPropertyRange | FunctionalDataProperty

SubDataPropertyOf := 'SubDataPropertyOf' '(' axiomAnnotations subDataPropertyExpression superDataPropertyExpression ')'
subDataPropertyExpression := DataPropertyExpression
superDataPropertyExpression := DataPropertyExpression

EquivalentDataProperties := 'EquivalentDataProperties' '(' axiomAnnotations DataPropertyExpression DataPropertyExpression { DataPropertyExpression } ')'

DisjointDataProperties := 'DisjointDataProperties' '(' axiomAnnotations DataPropertyExpression DataPropertyExpression { DataPropertyExpression } ')'

DataPropertyDomain := 'DataPropertyDomain' '(' axiomAnnotations DataPropertyExpression ClassExpression ')'

DataPropertyRange := 'DataPropertyRange' '(' axiomAnnotations DataPropertyExpression DataRange ')'

FunctionalDataProperty := 'FunctionalDataProperty' '(' axiomAnnotations DataPropertyExpression ')'

DatatypeDefinition := 'DatatypeDefinition' '(' axiomAnnotations Datatype DataRange ')'
"""


@dataclass
class DataPropertyAxiom(Axiom):
    pass


@dataclass
class SubDataPropertyOf(DataPropertyAxiom):
    subDataPropertyExpression: DataPropertyExpression
    superDataPropertyExpression: DataPropertyExpression
    annotations: List[Annotation] = empty_list()

    def to_functional(self, w: FunctionalWriter) -> FunctionalWriter:
        return self.annots(w, lambda: w + self.subDataPropertyExpression + self.superDataPropertyExpression)


@dataclass
class EquivalentDataProperties(DataPropertyAxiom):
    dataPropertyExpressions: List[DataPropertyExpression]
    annotations: List[Annotation] = empty_list()

    def __init__(self, *dataPropertyExpressions: DataPropertyExpression, annotations: List[Annotation] = None) -> None:
        self.dataPropertyExpressions = list(dataPropertyExpressions)
        self.annotations = annotations or []
        super().__init__()

    def to_functional(self, w: FunctionalWriter) -> FunctionalWriter:
        self.list_cardinality(self.dataPropertyExpressions, 'exprs', 2)
        return self.annots(w, lambda: w.iter(self.dataPropertyExpressions))


@dataclass
class DisjointDataProperties(DataPropertyAxiom):
    dataPropertyExpressions: List[DataPropertyExpression]
    annotations: List[Annotation] = empty_list()

    def __init__(self, *dataPropertyExpressions: DataPropertyExpression, annotations: List[Annotation] = None) -> None:
        self.dataPropertyExpressions = list(dataPropertyExpressions)
        self.annotations = annotations or []
        super().__init__()

    def to_functional(self, w: FunctionalWriter) -> FunctionalWriter:
        self.list_cardinality(self.dataPropertyExpressions, 'exprs', 2)
        return self.annots(w, lambda: w.iter(self.dataPropertyExpressions))


@dataclass
class DataPropertyDomain(DataPropertyAxiom):
    dataPropertyExpression: DataPropertyExpression
    classExpression: ClassExpression
    annotations: List[Annotation] = empty_list()

    def to_functional(self, w: FunctionalWriter) -> FunctionalWriter:
        return self.annots(w, lambda: w + self.dataPropertyExpression + ' ' + self.classExpression)


@dataclass
class DataPropertyRange(DataPropertyAxiom):
    dataPropertyExpression: DataPropertyExpression
    dataRange: DataRange
    annotations: List[Annotation] = empty_list()

    def to_functional(self, w: FunctionalWriter) -> FunctionalWriter:
        return self.annots(w, lambda: w + self.dataPropertyExpression + ' ' + self.dataRange)


@dataclass
class FunctionalDataProperty(DataPropertyAxiom):
    dataPropertyExpression: DataPropertyExpression
    annotations: List[Annotation] = empty_list()

    def to_functional(self, w: FunctionalWriter) -> FunctionalWriter:
        return self.annots(w, lambda: w + self.dataPropertyExpression)


@dataclass
class DataTypeDefinition(DataPropertyAxiom):
    datatype: Datatype
    datarange: DataRange
    annotations: List[Annotation] = empty_list()

    def to_functional(self, w: FunctionalWriter) -> FunctionalWriter:
        return self.annots(w, lambda: w + self.datatype + ' ' + self.datarange)
