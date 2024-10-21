import React from "react";
import { Table, Form } from "rsuite";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMicrochip } from "@fortawesome/free-solid-svg-icons";
import { faMoneyBillWave } from "@fortawesome/free-solid-svg-icons";
import { faSquarePollHorizontal } from "@fortawesome/free-solid-svg-icons";

const { Column, HeaderCell, Cell, ColumnGroup } = Table;
const icon_styles = {fontSize: '1.8em', color: "#248ae9"}
const header_styles = {display: "grid", gridAutoFlow: "column", gridColumnGap: 6, width: 60};

export const ProcTable = ({tableData}) => {
  let data = [];

  function CalculateResult(calc_type: string) {
    data = tableData.map(v => ({...v, Result: 1, Price: v.Price + "₽"}))
  };

  CalculateResult("123")

  return(
    <div style={{padding: 36, width: 1050}}>
      <Table
        shouldUpdateScroll={false}
        height={700}
        data={data}
        style={{borderRadius: 16}}
        headerHeight={80}
      >
        <ColumnGroup header={<div style={header_styles}><FontAwesomeIcon icon={faMicrochip} style={icon_styles}/> Processor</div>}>
          <Column width={250} align="left" fixed>
            <HeaderCell>{null}</HeaderCell>
            <Cell dataKey="Processor"/>
          </Column>
        </ColumnGroup>

        <ColumnGroup header={<div style={header_styles}><FontAwesomeIcon icon={faMoneyBillWave} style={icon_styles}/> Price</div>}>
          <Column width={160} align="left" fixed>
            <HeaderCell>{null}</HeaderCell>
            <Cell dataKey="Price"/>
          </Column>
        </ColumnGroup>

        <ColumnGroup >
          <Column width={160} align="left" fixed>
            <HeaderCell>{null}</HeaderCell>
            <Cell dataKey="Single Core"/>
          </Column>
        </ColumnGroup>

        <ColumnGroup>
          <Column width={160} align="left" fixed>
            <HeaderCell>{null}</HeaderCell>
            <Cell dataKey="Multi Core"/>
          </Column>
        </ColumnGroup>

        <ColumnGroup>
          <Column width={160} align="left" fixed>
            <HeaderCell>{null}</HeaderCell>
            <Cell dataKey="TDP"/>
          </Column>
        </ColumnGroup>

        <ColumnGroup header={<div style={header_styles}><FontAwesomeIcon icon={faSquarePollHorizontal} style={icon_styles}/> Result</div>}>
          <Column width={160} align="left" fixed>
            <HeaderCell>{null}</HeaderCell>
            <Cell dataKey="Result"/>
          </Column>
        </ColumnGroup>


      </Table>
    </div>
  );
}