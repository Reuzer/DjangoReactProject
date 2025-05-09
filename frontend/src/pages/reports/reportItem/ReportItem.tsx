import { FC } from "react";
import { PetReport } from "../../../api/types"
import styles from './ReportItem.module.css'
import Img from "../../../components/Img/Img";
import altPhoto from '../../../assets/alter.svg';
import { Link } from "react-router-dom";

interface Props {
    report: PetReport
}
 
const ReportItem: FC<Props> = ({report}) => {

    function toReadableDate(date: string) {
        if(date) {
            const readableDate = date.slice(0, 10);
            return readableDate;
        } else {
            return 'Не удалось прочесть дату'
        }
    }

    return (
        <>
            <Link to={`/reports/${report.id}`} className={styles.link}>
                <li className={styles.list__element}>                   
                    <Img altPhoto={altPhoto} photo={report.picture} className={styles.photo} />
                    <h2 className={styles.title}>{report.title}</h2>
                    <p className={styles.description}>{report.description}</p>
                    <p className={styles.date}>{toReadableDate(report.public_date)}</p>
                </li>
            </Link>
        </>
    );
}
 
export default ReportItem;