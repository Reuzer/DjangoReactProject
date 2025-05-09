import { FC } from "react";
import { PetReport } from "../../../api/types"
import styles from './ReportList.module.css'
import ReportItem from "../reportItem/ReportItem";

interface Props {
    reports: PetReport[]
}
 
const ReportList: FC<Props> = ({reports}) => {
    return (
            <ul className={styles.list}>
                {reports.map(report => 
                    <ReportItem report={report} />
                )}
            </ul>
    );
}
 
export default ReportList;